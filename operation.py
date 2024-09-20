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
def verify_files_integrity(f_src: Path, f_cpy: Path) -> bool:
    hash_src = get_md5(str(f_src))
    hash_cpy = get_md5(str(f_cpy))

    if hash_src == hash_cpy:
        return True
    else:
        return False


# If file in src was modified, then it is copied to cpy
# If there is a new file in src, then copy it into cpy
def copy_item(src: Path, cpy: Path):
    try:
        shutil.copy2(src, cpy)
    except Exception as e:
        print(e)


# If there is a new folder in src, then create one in cpy
def create_folder(new: Path):
    try:
        new.mkdir()
    except Exception as e:
        print(e)


# If an item was removed from the src, then remove if from cpy
def remove_item(item: Path, is_file: bool):
    if is_file:
        try:
            item.unlink()
        except Exception as e:
            print(e)
    else:
        try:
            shutil.rmtree(item)
        except Exception as e:
            print(e)
