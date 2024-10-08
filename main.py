import argparse
from pathlib import Path
import sys
from folder_content import Folder
import operation
import time

src = None
cpy = None
log_file = None

src_folders = []  # Folders that are inside the source folder
src_files = []  # Files that are inside the source folder
cpy_folders = []  # Folders that are inside the replica folder
cpy_files = []  # Files that are inside the replica folder

timeout = 0


# Checks the existence of the folders and the log file
def check_existence(source: str, copy: str):
    if not Path(source).exists():
        print("Source folder does not exist")
        return False

    if not Path(copy).exists():
        print("Copy folder does not exist")
        return False
    return True


# Check the existence of the folders and the integrity of the files inside copy folder
def update_copy():
    global timeout
    for f_src in src_folders:
        for f_cpy in cpy_folders:
            if not f_cpy.get_check() and f_src.get_path().name == f_cpy.get_path().name:
                f_cpy.set_check(True)
                f_src.set_check(True)
                break

        if not f_src.get_check():
            new_path = str(cpy.get_path()) + str(f_src.get_path()).replace(str(src.get_path()), "")
            operation.create_folder(Path(new_path))
            
            t = time.strftime("%H:%M:%S")
            log_file.write(f'{t} - Creating folder - {new_path}\n')
            print(f'{t} - Creating folder - {new_path}')

            timeout = 0

    for f_src in src_files:
        for f_cpy in cpy_files:
            if not f_cpy.get_check() and f_src.get_path().name == f_cpy.get_path().name:
                if not operation.verify_files_integrity(f_src.get_path(), f_cpy.get_path()):
                    operation.copy_item(f_src.get_path(), f_cpy.get_path())

                    t = time.strftime("%H:%M:%S")
                    log_file.write(f'{t} - {str(f_src.get_path())} was modified\n')
                    log_file.write(f'{t} - Copying file - {str(f_src.get_path())}\n')
                    print(f'{t} - {str(f_src.get_path())} was modified')
                    print(f'{t} - Copying file - {str(f_src.get_path())}')

                    timeout = 0

                f_cpy.set_check(True)
                f_src.set_check(True)
                break

        if not f_src.get_check():
            new_path = str(cpy.get_path()) + str(f_src.get_path()).replace(str(src.get_path()), "")
            operation.copy_item(f_src.get_path(), Path(new_path))

            t = time.strftime("%H:%M:%S")
            log_file.write(f'{t} - Adding new file - {new_path}\n')
            print(f'{t} - Adding new file - {new_path}')

            f_src.set_check(True)
            timeout = 0


# Remove files and folders that no longer exist in source folder
def remove_old_items():
    global timeout
    for f_cpy in cpy_files:
        if not f_cpy.get_check():
            operation.remove_item(f_cpy.get_path(), True)

            t = time.strftime("%H:%M:%S")
            log_file.write(f'{t} - Removing file - {str(f_cpy.get_path())}\n')
            print(f'{t} - Removing file - {str(f_cpy.get_path())}')

            timeout = 0

    for f_cpy in reversed(cpy_folders):
        if not f_cpy.get_check() :
            operation.remove_item(f_cpy.get_path(), False)

            t = time.strftime("%H:%M:%S")
            log_file.write(f'{t} - Removing folder - {str(f_cpy.get_path())}\n')
            print(f'{t} - Removing folder - {str(f_cpy.get_path())}')

            timeout = 0


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

    if not check_existence(source_path, copy_path):
        sys.exit(1)

    src = Folder(Path(source_path))
    cpy = Folder(Path(copy_path))
    log_file = open(log_path, "a")

    log_file.write(f'Synchronizing folders - {src.get_path().name} and {cpy.get_path().name}\n')
    print(f'Synchronizing folders - {src.get_path().name} and {cpy.get_path().name}')
    continue_ = True
    while continue_:
        # Get content
        src_files, src_folders = src.get_folder_items()
        cpy_files, cpy_folders = cpy.get_folder_items()

        update_copy()

        # Remove files and folders that no longer exist in source folder
        remove_old_items()

        time.sleep(sync_time)
        timeout += sync_time

        if timeout >= 300:
            answer = input(f'Would you like to continue? yes/no - ')
            if answer.lower() == 'yes':
                continue
            elif answer.lower() == 'no':
                continue_ = False
            else:
                print(f'Wrong answer -> exiting..')
                continue_ = False

    log_file.write(f'\n')
    log_file.close()
    print("End")

