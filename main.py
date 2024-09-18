import argparse
from pathlib import Path
import sys
from folder import InnerFolder

source_path = None
copy_path = None
log_path = None
sync_time = 0

src_folders = []  # Folders that are inside the source folder
src_files = []  # Files that are inside the source folder
cpy_folders = []  # Folders that are inside the replica folder
cpy_files = []  # Files that are inside the replica folder


# Get all items from the given folder
def get_folder_content(folder: str, belongs_to_source: bool):
    global src_folders, src_files, cpy_folders, cpy_files

    items = Path(folder).iterdir()
    for item in items:
        if belongs_to_source:
            if item.is_file():
                src_files.append(str(item))
            else:
                src_folders.append(InnerFolder(str(item), source_path))
        else:
            if item.is_file():
                cpy_files.append(str(item))
            else:
                cpy_folders.append(InnerFolder(str(item), copy_path))


# Checks the existence of the folders and the log file
def check_existence():
    if not Path(source_path).exists():
        print("Source folder does not exist")
        return False

    if not Path(copy_path).exists():
        print("Copy folder does not exist")
        return False

    if not Path(log_path).exists():
        print("Log file does not exist")
        return False
    return True


def check_folders_src_cpy():
    for f_src in src_folders:
        for f_cpy in cpy_folders:
            if f_cpy.get_check():
                continue
            if f_cpy.compare_relative_path(f_src.get_relative_path()):
                f_cpy.set_check(True)
                f_src.set_check(True)
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path", type=str, help="Source folder path")
    parser.add_argument("copy_path", type=str, help="Copy folder path")
    parser.add_argument("log_path", type=str, help="Log file path")
    parser.add_argument("sync_time", type=int, help="Synchronization time in seconds")
    args = parser.parse_args()

    source_path = args.source_path
    copy_path = args.copy_path
    log_path = args.log_path
    sync_time = args.sync_time

    if not check_existence():
        sys.exit(1)

    get_folder_content(source_path, True)
    get_folder_content(copy_path, False)
    check_folders_src_cpy()

'''
    while len(src_folders) > 0:
        f = src_folders.pop(0)
        get_folder_content(f.get_path(), True)

    while len(cpy_folders) > 0:
        f = cpy_folders.pop(0)
        get_folder_content(f.get_path(), False)
'''
