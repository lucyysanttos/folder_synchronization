class InnerFolder:
    def __init__(self, path: str):
        self.__check = False
        self.__path = path

    def get_path(self) -> str:
        return self.__path

    def get_check(self) -> bool:
        return self.__check

    def set_check(self, check):
        self.__check = check

    def compare_folder(self, source_folder: str, folder2: str) -> bool:
        if self.__path.replace(source_folder, "") == folder2:
            return True
        return False
