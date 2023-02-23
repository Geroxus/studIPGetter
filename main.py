from getpass import getpass


def login(userName: str, password: str) -> bool:
    return False


if __name__ == '__main__':
    userName = input("Enter your Username for StudIP: ")
    password = getpass()

    if login(userName, password):
        exit(3)

    exit(0)
