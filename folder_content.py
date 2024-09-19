from pathlib import Path


class File:
    def __init__(self, path: Path):
        self.__check = False
        self.__abs_path = path

    def get_check(self) -> bool:
        return self.__check

    def set_check(self, check):
        self.__check = check

    def get_path(self) -> Path:
        return self.__abs_path


class Folder:
    def __init__(self, path: Path):
        self.__check = False
        self.__abs_path = path

    def get_check(self) -> bool:
        return self.__check

    def set_check(self, check):
        self.__check = check

    def get_path(self) -> Path:
        return self.__abs_path

    # Get all items from the given folder
    def get_folder_items(self):
        files = []
        folders = []
        for item in self.__abs_path.rglob('*'):
            if item.is_file():
                files.append(File(item))
            else:
                folders.append(Folder(item))
        return files, folders
