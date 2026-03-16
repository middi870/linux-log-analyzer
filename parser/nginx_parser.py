import re
from datetime import datetime
from typing import Optional

from analyzer.event import Event
from parser.base_parser import BaseParser


NGINX_PATTERN = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) .* \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) .*" (?P<status>\d+)'
)


class NginxParser(BaseParser):

    def parse(self, line: str) -> Optional[Event]:

        match = NGINX_PATTERN.search(line)

        if not match:
            return None

        data = match.groupdict()

        timestamp = datetime.strptime(
            data["time"].split()[0],
            "%d/%b/%Y:%H:%M:%S"
        )

        status = int(data["status"])

        event_type = "HTTP_ERROR" if status >= 400 else "HTTP_REQUEST"

        return Event(
            timestamp=timestamp,
            host="nginx",
            service="nginx",
            pid=None,
            event_type=event_type,
            message=line,
            source_ip=data["ip"],
            severity="error" if status >= 500 else "info"
        )
