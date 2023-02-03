class EnumeratorException(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(f"{self.__class__.__name__}: {message}")
        self.code = code


class TargetSpecificationError(EnumeratorException):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message, code)


class FileReadError(EnumeratorException):
    def __init__(self, message: str, code: int = 1):
        super().__init__(message, code)
