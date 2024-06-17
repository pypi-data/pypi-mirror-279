import argparse
from .packtxt import pack_project_to_txt, unpack_txt_to_project

def main():
    parser = argparse.ArgumentParser(description='Pack a project directory to a .txt file or unpack a .txt file to a project directory.')
    
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for packing a project directory to a .txt file
    pack_parser = subparsers.add_parser('pack', help='Pack a project directory to a .txt file')
    pack_parser.add_argument('project_dir', type=str, help='The path to the project directory')
    pack_parser.add_argument('--branch', type=str, help='The Git branch to pack files from', default=None)  # Added branch argument
    pack_parser.add_argument('--output', type=str, help='The path to the output .txt file', default=None)

    # Subparser for unpacking a .txt file to a project directory
    unpack_parser = subparsers.add_parser('unpack', help='Unpack a .txt file to a project directory')
    unpack_parser.add_argument('txt_file', type=str, help='The path to the .txt file')
    unpack_parser.add_argument('--output', type=str, help='The path to the output directory', default=None)

    args = parser.parse_args()

    if args.command == 'pack':
        pack_project_to_txt(args.project_dir, args.branch, args.output)  # Pass branch argument
    elif args.command == 'unpack':
        unpack_txt_to_project(args.txt_file, args.output)

if __name__ == '__main__':
    main()
