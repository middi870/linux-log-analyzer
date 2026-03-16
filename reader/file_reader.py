from pathlib import Path
from typing import Iterator


class FileReader:
    """
    Efficient file reader that streams logs line-by-line.
    Suitable for large log files.
    """

    def __init__(self, filepath: str):
        self.path = Path(filepath)

        if not self.path.exists():
            raise FileNotFoundError(f"Log file not found: {filepath}")

    def read_lines(self) -> Iterator[str]:
        """
        Yield log lines one by one.
        """
        with self.path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                yield line.rstrip("\n")
