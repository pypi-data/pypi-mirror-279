import os
import shutil
import argparse


def copy_gitignore_to_gpt_ignore(gitignore_file, gpt_ignore_file):
    if not os.path.exists(gpt_ignore_file) and os.path.exists(gitignore_file):
        shutil.copy(gitignore_file, gpt_ignore_file)
        print(f"Copied {gitignore_file} to {gpt_ignore_file}")


def load_ignore_list(ignore_file):
    ignore_list = []
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r') as f:
            ignore_list = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ignore_list


def should_ignore(path, ignore_list):
    for ignore_pattern in ignore_list:
        if os.path.isabs(ignore_pattern):
            if path == ignore_pattern or path.startswith(ignore_pattern + os.sep):
                return True
        else:
            if ignore_pattern in path:
                return True
    return False


def read_all_files(root_dir, ignore_list, allowed_extensions):
    all_code = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter ignored directories
        filtered_dirnames = []
        for dirname in dirnames:
            if not should_ignore(os.path.join(dirpath, dirname), ignore_list):
                filtered_dirnames.append(dirname)
        dirnames[:] = filtered_dirnames
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if should_ignore(file_path, ignore_list):
                continue
            file_extension = os.path.splitext(filename)[1]
            if file_extension not in allowed_extensions:
                continue
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    file_content = f.read()
                    annotation = f"File: {file_path}\nType: {file_extension}\n\n"
                    all_code.append(annotation + file_content + '\n\n')
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    return all_code


def write_to_output_file(output_file, all_code):
    with open(os.path.join(root_dir, output_file), 'w') as f:
        for code in all_code:
            f.write(code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect code from project directory.")
    parser.add_argument("root_dir", type=str, help="Path to the project directory")
    parser.add_argument("--output_file", type=str, default="all_code.txt", help="Output filename (default: all_code.txt)")
    args = parser.parse_args()

    root_dir = args.root_dir
    output_file = args.output_file

    # Copy .gitignore to .gpt-ignore if .gpt-ignore does not exist
    gitignore_file = os.path.join(root_dir, '.gitignore')
    gpt_ignore_file = os.path.join(root_dir, '.gpt-ignore')
    copy_gitignore_to_gpt_ignore(gitignore_file, gpt_ignore_file)

    ignore_list = load_ignore_list(gpt_ignore_file)

    # Define the allowed file extensions for programming languages
    allowed_extensions = {'.py', '.java', '.c', '.cpp', '.html', '.css', '.js', '.ts', '.rb', '.php', '.cs', '.swift', '.go', '.rs', '.kt', '.m', '.h', '.sh'}

    all_code = read_all_files(root_dir, ignore_list, allowed_extensions)
    write_to_output_file(output_file, all_code)

    print(f"All code has been written to {output_file}")
