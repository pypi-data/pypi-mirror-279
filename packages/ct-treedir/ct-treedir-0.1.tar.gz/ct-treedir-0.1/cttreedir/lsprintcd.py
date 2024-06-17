import os

from .help import load_ignore_list, create_directory_tree

def list_subdirectories(parent_directory, ignore_list):
    try:
        subdirectories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]
        subdirectories = [d for d in subdirectories if not should_ignore(d, ignore_list)]
        return subdirectories
    except FileNotFoundError:
        print(f"Directory Not Found: {parent_directory}")
        return []
    except PermissionError:
        print(f"Permission Denied: {parent_directory}")
        return []

def select_subdirectories(subdirectories):
    print("Subdirectories:")
    for index, subdir in enumerate(subdirectories):
        print(f"{index}: {subdir}")

    selected_indices = input("Enter the indices you want generated: ").split(',')
    selected_indices = [int(i.strip()) for i in selected_indices if i.strip().isdigit()]

    return [subdirectories[i] for i in selected_indices if 0 <= i < len(subdirectories)]

def run_lsprintcd():
    ignore_file_path = '.ignorelist'

    ignore_string = input("Enter custom .ignorelist: ").strip()
    ignore_list = ignore_string.split(',') if ignore_string else []
    ignore_list.extend(load_ignore_list(ignore_file_path))

    author_string = input("Enter author name: ").strip()

    parent_directory = input("Enter the parent directory: ")
    subdirectories = list_subdirectories(parent_directory, ignore_list)

    if not subdirectories:
        print("No subdirectories found or all are ignored.")
    else:
        selected_subdirectories = select_subdirectories(subdirectories)

        for subdirectory in selected_subdirectories:
            user_directory = os.path.join(parent_directory, subdirectory)
            create_directory_tree(user_directory, author_string, ignore_list)
