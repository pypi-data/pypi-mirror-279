from .help import load_ignore_list, create_directory_tree

def run_printcd():
    ignore_file_path = '.ignorelist'

    ignore_string = input("Enter custom .ignorelist: ").strip()
    ignore_list = ignore_string.split(',') if ignore_string else load_ignore_list(ignore_file_path)

    author_string = input("Enter author name: ").strip()

    user_directory = input("Enter the directory path: ")

    create_directory_tree(user_directory, author_string, ignore_list)