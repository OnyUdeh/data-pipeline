import sys

import requests


def main():
    print("Hello from my data pipeline!")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Python location: {sys.executable}")
    print(f"requests version: {requests.__version__}")


if __name__ == "__main__":
    main()