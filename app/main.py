import sys
import shutil

builtins: list = ["echo", "exit", "type"]


def main():
    while True:
        prompt: str = "$ "
        sys.stdout.write(prompt)
        command: str = input().strip()
        command: dict = {
            "base": command.split(" ")[0],
            "arguments": command.split(" ")[1:],
        }

        match command["base"]:
            case "exit":
                exit()
            case "echo":
                print(" ".join(command["arguments"]))
            case "type":
                if command["arguments"][0] in builtins:
                    print(f"{command['arguments'][0]} is a shell builtin")
                elif path := shutil.which(command["arguments"][0]):
                    print(f"{command['arguments'][0]} is {path}")
                else:
                    print(f"{command['arguments'][0]}: not found")

            case "":
                pass
            case _:
                print(f"{command['base']}: command not found")


if __name__ == "__main__":
    main()