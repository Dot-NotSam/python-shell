import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")

    command = input()
    print(f"{command}: command not found")
    
    if(command == "exit"):
        sys.exit()
    main()

    exit



if __name__ == "__main__":
    main()
