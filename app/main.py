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

        # Check for output redirection
        output_file = None
        if ">" in command:
            # Split by > to separate command from redirection
            cmd_part, redirect_part = command.split(">", 1)
            # Handle both > and 1>
            redirect_part = redirect_part.lstrip()
            if redirect_part.startswith("1"):
                redirect_part = redirect_part[1:].lstrip()
            output_file = redirect_part.strip()
            
            # Re-parse the command part
            parts = cmd_part.split(" ", 1)
            cmd = parts[0]
            args = parts[1] if len(parts) > 1 else ""

        if cmd == "exit":
            return
        elif cmd == "echo":
            output = echo(args)
            if output_file:
                with open(output_file, "w") as f:
                    f.write(output + "\n")
            else:
                print(output)
        elif cmd == "type":
            output = type(args)
            if output_file:
                with open(output_file, "w") as f:
                    f.write(output + "\n")
            else:
                print(output)
        elif cmd == "pwd":
            output = os.getcwd()
            if output_file:
                with open(output_file, "w") as f:
                    f.write(output + "\n")
            else:
                print(output)
        elif cmd == "cd":
            # Handle ~ character
            if args == "~":
                args = os.environ.get("HOME", "")
            
            # Absolute Path or expanded path
            if args:
                try:
                    os.chdir(args)
                except FileNotFoundError:
                    print(f"cd: {args}: No such file or directory")
        # Custom Program
        elif find_exec(cmd):  # Confirmed correct!
            if output_file:
                with open(output_file, "w") as f:
                    subprocess.run([cmd] + cmd_part.split()[1:], stdout=f)
            else:
                subprocess.run([cmd] + command.split()[1:])
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()