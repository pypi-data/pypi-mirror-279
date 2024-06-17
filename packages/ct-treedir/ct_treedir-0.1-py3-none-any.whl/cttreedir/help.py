import os
import re
import shutil
import getpass
import datetime
from colorama import init

init()

def load_ignore_list(ignore_file):
    ignore_set = set()
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r') as file:
            for line in file:
                pattern = line.strip()
                if pattern:
                    ignore_set.add(pattern)
    return ignore_set

def should_ignore(item, ignore_list):
    for ignore in ignore_list:
        if ignore.startswith('.') and item.endswith(ignore):
            return True
        elif ignore == item:
            return True
    return False

def natural_sort_key(s):
    """ Sort key function to sort strings by numerical content. """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def list_files_recursively(directory, prefix='', file=None, base_directory=None, ignore_list=None):
    try:
        items = os.listdir(directory)
        items.sort(key=natural_sort_key)
    except PermissionError:
        file.write(f"{prefix}Permission Denied: {directory}\n")
        return
    except FileNotFoundError:
        file.write(f"{prefix}Directory Not Found: {directory}\n")
        return

    for index, item in enumerate(items):
        if should_ignore(item, ignore_list):
            continue
        item_path = os.path.join(directory, item)
        connector = '└──' if index == len(items) - 1 else '├──'
        file.write(f"{prefix}{connector} {item}\n")
        if os.path.isdir(item_path):
            extension = '    ' if index == len(items) - 1 else '│   '
            list_files_recursively(item_path, prefix + extension, file, base_directory, ignore_list)

def get_next_version_number(directory):
    versions = []
    for folder in os.listdir(directory):
        if re.match(r'\d{3}', folder) or folder == '000':
            versions.append(int(folder))
    
    if not versions:
        return '001'
    
    versions.sort()
    next_version = versions[-1] + 1
    if next_version == 1000:
        next_version = 0
    
    while True:
        version_str = f'{next_version:03d}'
        if not os.path.exists(os.path.join(directory, version_str)):
            return version_str
        next_version += 1
        if next_version == 1000:
            next_version = 0

def create_directory_tree(user_directory, author_string, ignore_list=None):
    absolute_directory = os.path.abspath(user_directory)

    if not getpass.getuser() == "root":
        print("Administrator required. Please try sudo.")
        return

    previous_versions_dir = os.path.join(absolute_directory, '.directory')
    if not os.path.exists(previous_versions_dir):
        os.makedirs(previous_versions_dir)

    next_version = get_next_version_number(previous_versions_dir)
    new_version_dir = os.path.join(previous_versions_dir, next_version)
    if not os.path.exists(new_version_dir):
        os.makedirs(new_version_dir)

    original_tree_path = os.path.join(absolute_directory, 'tree.cwd')
    version_tree_path = os.path.join(new_version_dir, 'tree.cwd')

    today = datetime.datetime.today()
    tree_content = (
        "Generated Directory Tree\n"
        f"{today.strftime('%Y-%m-%d')}T{today.strftime('%H:%M:%S')}\n"
        f".directory/{next_version}/tree.cwd\n\n"
        f"{author_string}\n\n"
    )

    with open(original_tree_path, 'w') as file:
        file.write(tree_content)
        list_files_recursively(absolute_directory, '', file, absolute_directory, ignore_list)

    shutil.copyfile(original_tree_path, version_tree_path)

    print(f"The tree has been written to: '{original_tree_path}'.")
