from pathlib import Path
from typing import Iterator


class DirectoryReader:
    """
    Reads all files inside a directory sequentially.

    Useful for analyzing entire log directories such as /var/log.
    """

    def __init__(self, directory: str):

        self.directory = Path(directory)

        if not self.directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        if not self.directory.is_dir():
            raise ValueError(f"Not a directory: {directory}")

    def read_lines(self) -> Iterator[str]:

        for file in sorted(self.directory.iterdir()):

            if not file.is_file():
                continue

            try:
                with file.open("r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        yield line.rstrip("\n")
            except PermissionError:
                # skip files we cannot read
                continue
