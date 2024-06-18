class GeneralException(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class NoBucketFound(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class NoCredentialsFound(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)

class FileNotFoundException(Exception):
    def __init__(self) -> None:
        super().__init__(f"File not found")

class FileAlreadyExists(Exception):
    def __init__(self) -> None:
        super().__init__(f"File already exists")