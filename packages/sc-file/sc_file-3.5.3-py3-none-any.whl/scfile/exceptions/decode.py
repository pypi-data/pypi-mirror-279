from pathlib import Path

from scfile.utils.types import PathLike

from .base import ScFileException


class FileDecodingError(ScFileException):
    """Exception occurring when file decoding."""

    def __init__(self, path: PathLike):
        self.path = Path(path)

    @property
    def posix_path(self) -> str:
        return self.path.as_posix()


class FileParsingError(ScFileException):
    """Exception occurring due incorrect file parsing. (Or file incorrect itself)."""

    pass


class FileUnsupportedError(ScFileException):
    """Exception occurring intentionally due incorrect file parsing."""

    pass
