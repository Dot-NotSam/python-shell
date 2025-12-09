import sys
import os
import subprocess

commands = {
    "exit": lambda *args: sys.exit(int(args[0]) if args else 0),
    "echo": lambda *args: print(" ".join(args)),
    "type": lambda *args: check_command_type(args[0]) if args else None,
    "pwd": lambda *args: print(os.getcwd()),
}


def check_command_type(command):
    if command in commands:
        print(f"{command} is a shell builtin")
    else:
        path_env = os.environ.get("PATH", "")
        for path_dir in path_env.split(os.pathsep):
            full_path = os.path.join(path_dir, command)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                print(f"{command} is {full_path}")
                return
        print(f"{command}: not found")


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command_args = input().split()
        command = command_args[0]

        if command not in commands:
            for path_dir in os.environ.get("PATH", "").split(os.pathsep):
                full_path = os.path.join(path_dir, command)
                if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                    subprocess.run(command_args)
                    break
            else:
                print(f"{command}: command not found")
            continue

        commands[command](*command_args[1:])


if __name__ == "__main__":
    main()