import sys
import os


def run(bin_name: str):
    path = os.path.join(os.path.dirname(__file__), "files", bin_name)
    args = sys.argv[1:]
    os.execv(path, [bin_name] + args)


def main():
    os_name = os.name
    if os_name == "posix":
        path = "git"
    elif os_name == "nt":
        path = "git.exe"
    else:
        raise NotImplementedError(f"Unsupported OS: {os_name}")

    run(path)


if __name__ == "__main__":
    main()
