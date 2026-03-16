import re
from datetime import datetime
from typing import Optional

from analyzer.event import Event
from parser.base_parser import BaseParser


SSH_FAIL_PATTERN = re.compile(
    r"(?P<ts>\w+\s+\d+\s+\d+:\d+:\d+)\s+(?P<host>\S+)\s+sshd\[(?P<pid>\d+)\]:\s+Failed password .* from (?P<ip>\d+\.\d+\.\d+\.\d+)"
)

SSH_SUCCESS_PATTERN = re.compile(
    r"(?P<ts>\w+\s+\d+\s+\d+:\d+:\d+)\s+(?P<host>\S+)\s+sshd\[(?P<pid>\d+)\]:\s+Accepted password .* from (?P<ip>\d+\.\d+\.\d+\.\d+)"
)


class AuthLogParser(BaseParser):

    def parse(self, line: str) -> Optional[Event]:

        match = SSH_FAIL_PATTERN.search(line)
        if match:
            data = match.groupdict()

            ts = datetime.strptime(data["ts"], "%b %d %H:%M:%S")
            ts = ts.replace(year=datetime.now().year)

            return Event(
                timestamp=ts,
                host=data["host"],
                service="sshd",
                pid=int(data["pid"]),
                event_type="AUTH_FAIL",
                message=line,
                source_ip=data["ip"],
                severity="warning",
            )

        match = SSH_SUCCESS_PATTERN.search(line)
        if match:
            data = match.groupdict()

            ts = datetime.strptime(data["ts"], "%b %d %H:%M:%S")
            ts = ts.replace(year=datetime.now().year)

            return Event(
                timestamp=ts,
                host=data["host"],
                service="sshd",
                pid=int(data["pid"]),
                event_type="AUTH_SUCCESS",
                message=line,
                source_ip=data["ip"],
                severity="info",
            )

        return None
