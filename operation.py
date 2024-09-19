from pathlib import Path
import shutil
import hashlib


def get_md5(file: str):
    md5 = hashlib.md5()
    with open(file, 'rb') as f:
        while chunk := f.read(4096):
            md5.update(chunk)
    return md5.hexdigest()


# Use MD5 to check if the file was modified
def verify_files_integrity(f_scr: Path, f_cpy: Path) -> bool:
    hash_scr = get_md5(str(f_scr))
    hash_cpy = get_md5(str(f_cpy))

    if hash_scr == hash_cpy:
        return True
    else:
        print(f'          {str(f_cpy)} was modified')
        return False


# If file in src was modified, then it is copied to cpy
# If there is a new file in src, then copy it into cpy
def copy_item(src: Path, cpy: Path, is_new: bool):
    if not cpy.parent.exists():
        create_folder(cpy.parent)
    shutil.copy2(src, cpy)
    if is_new:
        print(f'          Adding new file - {str(cpy)}')
    else:
        print(f'          Copying file - {str(cpy)}')
    # Log msg cmd + file -> it changes based os the var is_new


# If there is a new folder in src, then create one in cpy
def create_folder(new: Path):
    if not new.parent.exists():
        create_folder(new.parent)
    try:
        new.mkdir()
        print(f'          Creating folder - {str(new)}')
    except Exception as e:
        print(e)


# If an item was removed from the src, then remove if from cpy
def remove_item(item: Path, is_file: bool):
    if is_file:
        try:
            item.unlink()
            print(f'          Removing file - {str(item)}')
        except Exception as e:
            print(e)
    else:
        try:
            shutil.rmtree(item)
            print(f'          Removing folder - {str(item)}')
        except Exception as e:
            print(e)
