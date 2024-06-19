class NotJsonFileError(Exception):
    def __init__(self, file_path, message="File '{}' is not a JSON file"):
        self.file_path = file_path
        self.message = message.format(file_path)
        super().__init__(self.message)


class KeyDuplicateError(Exception):
    def __init__(self, key, message="Key '{}' already exists"):
        self.key = key
        self.message = message.format(key)
        super().__init__(self.message)


class KeyNotFoundError(Exception):
    def __init__(self, key, message="Key '{}' not found"):
        self.key = key
        self.message = message.format(key)
        super().__init__(self.message)