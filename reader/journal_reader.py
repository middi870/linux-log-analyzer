import subprocess
from typing import Iterator


class JournalReader:
    """
    Streams logs from systemd journal using journalctl.
    """

    def __init__(self, unit: str = None):

        cmd = ["journalctl", "-o", "short"]

        if unit:
            cmd += ["-u", unit]

        cmd += ["--no-pager"]

        self.cmd = cmd

    def read_lines(self) -> Iterator[str]:

        process = subprocess.Popen(
            self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            yield line.rstrip("\n")
