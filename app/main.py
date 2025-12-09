import sys, os, shutil, shlex, subprocess

# list can contain elements of multiple data types
builtins: list = ["exit", "echo", "type", "pwd"]
PATH = os.getenv("PATH", "")
paths = PATH.split(":")
HOME = os.getenv("HOME", "")


def find_exec(cmd: str):
    for path in paths:
        full_path = f"{path}/{cmd}"
        try:
            with open(full_path):
                # os.X_OK: Checks if the path is executable.
                if os.access(full_path, os.X_OK):
                    return full_path
        except FileNotFoundError:
            continue
    return None


def main():
    while True:
        sys.stdout.write("$ ")
        command_inp: str = input().strip()
        # removes all leading and trailing whitespace characters, including spaces, tabs (\t), newlines (\n), and carriage returns (\r)
        # reassigning the command variable
        command: dict = {
            "base": shlex.split(command_inp)[0],
            "args": shlex.split(command_inp)[1:],
        }
        # print(shlex.split(command_inp))
        if ">" in command_inp or "1>" in command_inp:
            os.system(command_inp)
            continue
        match command["base"]:
            case "exit":
                exit()
            case "echo":
                # separator.join(iterable_of_strings)
                print(" ".join(command["args"]))
            case "type":
                if command["args"][0] in builtins:
                    print(f"{command["args"][0]} is a shell builtin")
                # shutil.which() return the path to an executable which would be run if the given cmd was called. If no cmd would be called, return None.
                elif path := shutil.which(command["args"][0]):
                    print(f"{command["args"][0]} is {path}")
                # path=shutil.which(command["args"][0])
                # if path:
                #     print(f"{command["args"][0]} is path")
                else:
                    print(f"{command["args"][0]}: not found")
            case "pwd":
                print(os.getcwd())
            case "cd":
                if command["args"][0] == "~":
                    os.chdir(HOME)
                # os.chdir("test_folder")
                # os.path.isdir(directory_path)
                elif os.path.isdir(command["args"][0]):
                    os.chdir(command["args"][0])
                else:
                    print(f"cd: {command["args"][0]}: No such file or directory")
            case _:
                if path := find_exec(command["base"]):
                    subprocess.run([command["base"]] + command["args"], executable=path)
                else:
                    print(f"{command['base']}: command not found")
        pass


if __name__ == "__main__":
    main()