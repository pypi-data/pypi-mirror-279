class FileExtensionError(ValueError):
    def __init__(self,
                 message="File extension '.gz' is missing"):
        self.message = message
        super().__init__(self.message)


class ModeStrError(TypeError):
    def __init__(self, message="Unzip mode must be a str"):
        self.message = message
        super().__init__(self.message)


class ModeNameError(ValueError):
    def __init__(self, message="Unzip mode must be either 'to_ram' or 'to_file' (default)"):
        self.message = message
        super().__init__(self.message)


class MaxGzipSizeError(ValueError):
    def __init__(self,
                 message='Uncompressed file size exceeds 2 GB'):
        self.message = message
        super().__init__(self.message)


class FilePathError(TypeError):
    def __init__(self, message="Filename must be a str"):
        self.message = message
        super().__init__(self.message)


class EmptyFileError(ValueError):
    def __init__(self, message="The file size is zero"):
        self.message = message
        super().__init__(self.message)


class RemiderNotZeroError(ValueError):
    def __init__(self,
                 message='The number of blocks in the file is not an integer '
                         '(the binary file contains data that does not relate '
                         'to any of the blocks)'):
        self.message = message
        super().__init__(self.message)


class NumberOfBlocksIsZeroError(ValueError):
    def __init__(self, message='The binary file contains a non-integer number of blocks '
                               '(possibly the file is empty)'):
        self.message = message
        super().__init__(self.message)


class NotEnoughBlocksInFileError(ValueError):
    def __init__(self, message='Missing required blocks in the binary file'):
        self.message = message
        super().__init__(self.message)


class FileNameError(ValueError):
    def __init__(self, message="Incorrect file name length or absence of special characters 'j'/'f' in the name"):
        self.message = message
        super().__init__(self.message)
