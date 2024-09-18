class InnerFolder:
    def __init__(self, path: str, src_folder: str):
        self.__check = False
        self.__abs_path = path
        self.__rtv_path = path.replace(src_folder, "")

    def get_absolute_path(self) -> str:
        return self.__abs_path

    def get_check(self) -> bool:
        return self.__check

    def get_relative_path(self) -> str:
        return self.__rtv_path

    def set_check(self, check):
        self.__check = check

    def compare_relative_path(self, f: str) -> bool:
        if self.__rtv_path == f:
            return True
        return False
