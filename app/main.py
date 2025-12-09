from datetime import datetime
import os
import subprocess
import sys
import shutil
import shlex
from xmlrpc.client import DateTime


def command_type(command):
    if command in commands:
        print(f"{command} is a shell builtin")
    elif path := shutil.which(command):
        print(f"{command} is {path}")
    else:
        print(f"{command}: not found")


def change_path(path):
    if path != "~":
        try:
            os.chdir(path)
        except FileNotFoundError:
            print(f"cd: {path}: No such file or directory")
    else:
        os.chdir(os.environ["HOME"])


def getCurrentPath():
    if os.getcwd() == os.environ["HOME"]:
        return "~"
    else:
        return os.getcwd()


commands = {
    "exit": lambda: os._exit(0),
    "echo": lambda *args: print(" ".join(args)),
    "type": lambda command: command_type(command),
    "pwd": lambda: print(os.getcwd()),
    "cd": lambda path: change_path(path),
}


def main():
    while True:
        # sys.stdout.write(f"{datetime.now().date()} | { getCurrentPath() } $ ")
        sys.stdout.write(f"$ ")

        command_with_args = input().strip()
        command_with_args = shlex.split(command_with_args)

        command = command_with_args[0]

        if (
            ">" in command_with_args
            or "1>" in command_with_args
            or "2>" in command_with_args
            or ">>" in command_with_args
            or "1>>" in command_with_args
            or "2>>" in command_with_args
        ):
            os.system(" ".join(command_with_args))
            continue

        if command in commands:
            commands[command](*command_with_args[1:])
            continue
        elif path := shutil.which(command):
            subprocess.run(command_with_args)
            continue

        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
