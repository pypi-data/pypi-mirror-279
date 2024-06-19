import sys
from subprocess import Popen, PIPE, STDOUT
from time import ctime
import os


class Q2Terminal:
    def __init__(self, terminal=None, echo=False, callback=None, encoding="utf-8"):
        self.echo = False
        self.callback = None
        self.shell = False
        self.locale_encoding = encoding
        if terminal is None:
            if "win32" in sys.platform:
                terminal = "powershell"
            elif "darwin" in sys.platform:
                terminal = "zsh"
            else:
                terminal = "bash"
        if "win32" in sys.platform:
            self.shell = True
            os.system("chcp 65001")
        self.proc = Popen(
            [terminal],
            shell=self.shell,
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT,
        )
        self.run("echo 0")
        self.echo = echo
        self.callback = callback
        self.exit_code = None

    def run(self, cmd="", echo=False, callback=None):
        if len(cmd) <= 0:
            return ""
        if echo or self.echo:
            print(f"{ctime()}> {cmd}>")
        _callback = callback if callback else self.callback
        self.exit_code = None
        if cmd[0] in ('"', "'") and "win32" in sys.platform:
            cmd = f"&{cmd}"
        cmd = f"{cmd}; echo $?;echo q2eoc\n"
        self.proc.stdin.writelines([bytes(cmd, "utf8")])
        self.proc.stdin.flush()
        rez = []
        # skip first line of output for Windows powershell
        first_line = True if "win32" in sys.platform else False
        while self.proc.poll() is None:
            line = (
                self.proc.stdout.readline().decode(self.locale_encoding, errors="backslashreplace").rstrip()
            )
            if not line:
                continue
            if first_line:
                first_line = False
                continue

            if line.strip() == "q2eoc":
                if rez:
                    self.exit_code = rez.pop().strip()
                    if self.exit_code.isdigit():
                        self.exit_code = int(self.exit_code)
                    elif self.exit_code == "True":
                        self.exit_code = 0
                    elif self.exit_code == "False":
                        self.exit_code = 1
                break
            elif line == "":
                continue
            else:
                rez.append(line)
                if echo or self.echo:
                    print(f"{ctime()}:\t{line}")
                if callable(_callback):
                    _callback(line)

        return rez

    def close(self):
        self.proc.terminate()
