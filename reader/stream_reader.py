import time
from pathlib import Path
from typing import Iterator


class StreamReader:
    """
    Continuously follow a log file (similar to `tail -f`).
    """

    def __init__(self, filepath: str, interval: float = 0.5):
        self.path = Path(filepath)
        self.interval = interval

        if not self.path.exists():
            raise FileNotFoundError(f"Log file not found: {filepath}")

    def follow(self) -> Iterator[str]:
        with self.path.open("r", encoding="utf-8", errors="ignore") as f:
            f.seek(0, 2)

            while True:
                line = f.readline()

                if not line:
                    time.sleep(self.interval)
                    continue

                yield line.rstrip("\n")
