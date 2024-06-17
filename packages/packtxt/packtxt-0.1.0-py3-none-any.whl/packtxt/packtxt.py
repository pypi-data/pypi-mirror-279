import os
import zipfile
import shutil
import subprocess

def pack_project_to_txt(project_dir, branch=None, output_path=None):
    if not os.path.isdir(project_dir):
        raise ValueError(f"{project_dir} is not a valid directory")
    
    original_dir = os.getcwd()
    os.chdir(project_dir)
    
    if branch:
        result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], capture_output=True, text=True)
        if 'true' not in result.stdout:
            os.chdir(original_dir)
            raise ValueError(f"{project_dir} is not a Git repository")
        
        current_branch = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True).stdout.strip()
        result = subprocess.run(['git', 'checkout', branch], capture_output=True, text=True)
        if result.returncode != 0:
            subprocess.run(['git', 'checkout', current_branch], capture_output=True, text=True)
            os.chdir(original_dir)
            raise ValueError(f"Branch '{branch}' does not exist")
        print(f"Switched to branch '{branch}'")
        print(f"Contents of '{project_dir}' after switching to branch '{branch}':")
        for root, dirs, files in os.walk('.'):
            for name in dirs:
                print(os.path.join(root, name))
            for name in files:
                print(os.path.join(root, name))

    if not output_path:
        output_path = os.path.join(original_dir, os.path.basename(project_dir) + '.txt')
    
    zip_file = output_path.replace('.txt', '.zip')
    
    # Create a zip file from the project directory
    print(f"Packing directory '{project_dir}' to '{zip_file}'")
    shutil.make_archive(base_name=zip_file.replace('.zip', ''), format='zip', root_dir='.')
    
    # Rename the zip file to .txt
    os.rename(zip_file, output_path)
    print(f"Renamed '{zip_file}' to '{output_path}'")
    
    if branch:
        subprocess.run(['git', 'checkout', current_branch], capture_output=True, text=True)
        print(f"Switched back to branch '{current_branch}'")
    os.chdir(original_dir)
    
    print(f"Packed {project_dir} into {output_path}")

def unpack_txt_to_project(txt_file, output_dir=None):
    if not os.path.isfile(txt_file):
        raise ValueError(f"{txt_file} is not a valid file")
    
    if not output_dir:
        # Default output directory is the same directory as the .txt file with the same base name as the .txt file
        output_dir = os.path.join(os.path.dirname(os.path.abspath(txt_file)), os.path.basename(txt_file).replace('.txt', ''))
    
    zip_file = txt_file.replace('.txt', '.zip')
    os.rename(txt_file, zip_file)
    
    # Extract the zip file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    
    # Rename the zip file back to .txt
    os.rename(zip_file, txt_file)
    print(f"Unpacked {txt_file} into {output_dir}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Pack and unpack project directories into/from .txt files.")
    subparsers = parser.add_subparsers(dest="command")

    pack_parser = subparsers.add_parser("pack", help="Pack a directory into a .txt file")
    pack_parser.add_argument("directory_path", type=str, help="The directory to pack")
    pack_parser.add_argument("--branch", type=str, help="The Git branch to pack files from", default=None)
    pack_parser.add_argument("--output", type=str, help="The output .txt file path", default=None)

    unpack_parser = subparsers.add_parser("unpack", help="Unpack a .txt file into a directory")
    unpack_parser.add_argument("txt_file", type=str, help="The .txt file to unpack")
    unpack_parser.add_argument("--output", type=str, help="The output directory path", default=None)

    args = parser.parse_args()

    if args.command == "pack":
        pack_project_to_txt(args.directory_path, args.branch, args.output)
    elif args.command == "unpack":
        unpack_txt_to_project(args.txt_file, args.output)
