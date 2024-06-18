import argparse
from pkg_vers.package_manager import get_pkg_vers 

def get_versions(paths):
    packages = get_pkg_vers(paths)
    for name, version in packages.items():
        print(f"{name}: {version}")

def main():
    parser = argparse.ArgumentParser(description='Package Manager CLI')
    subparsers = parser.add_subparsers(dest='command')

    get_versions_parser = subparsers.add_parser('get_versions', help='Get installed package versions')
    get_versions_parser.add_argument('paths', nargs='*', help='File paths, list of file paths, or folder path')

    args = parser.parse_args()

    if args.command == 'get_versions':
        get_versions(args.paths)

if __name__ == "__main__":
    main()
