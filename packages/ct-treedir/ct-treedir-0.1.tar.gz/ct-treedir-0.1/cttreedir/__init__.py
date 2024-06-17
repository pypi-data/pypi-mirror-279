import argparse
from .printcd import run_printcd
from .lsprintcd import run_lsprintcd

def main():
    parser = argparse.ArgumentParser(description="Command Terminal: Tree Directory Generator")
    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser("generate", help="-> generate directory tree")
    generate_parser.add_argument("--parent", action="store_true", help="-> specify if you want to scan for subdirectories")

    args = parser.parse_args()

    if args.command == "generate":
        if args.parent:
            run_lsprintcd()
        else:
            run_printcd()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
