import sys
import os
import subprocess


def main():
    # Uncomment this block to pass  the first stage
    # sys.stdout.write("$ ")
    builtin_cmds = {"exit", "echo", "type", "pwd", "cd"}

    def find_exec(cmd):
        # PATH navigation
        # get PATH env var and split it
        path_env = os.environ.get("PATH", "")
        dirs = path_env.split(os.pathsep)
        # search through each dir
        for d in dirs:
            full_path = os.path.join(d, cmd)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                return full_path

        return None

    def echo(args):
        return args

    def type(args):
        # built in
        if args in builtin_cmds:
            return f"{args} is a shell builtin"
        elif full_path := find_exec(args):
            return f"{args} is {full_path}"
        else:
            return f"{args}: not found"

    # Wait for user input
    while True:
        command = input("$ ")
        parts = command.split(" ", 1)
        cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        if cmd == "exit":
            return
        elif cmd == "echo":
            print(echo(args))
        elif cmd == "type":
            print(type(args))
        elif cmd == "pwd":
            print(os.getcwd())
        elif cmd == "cd":
            # Absolute Path
            if args:
                try:
                    os.chdir(args)
                except FileNotFoundError:
                    print(f"cd: {args}: No such file or directory")

            # Relative Path
            pass
        # Custom Program
        elif find_exec(cmd):  # Confirmed correct!
            subprocess.run([cmd] + command.split()[1:])
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
