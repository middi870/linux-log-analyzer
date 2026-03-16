import re
from datetime import datetime
from typing import Optional

from analyzer.event import Event
from parser.base_parser import BaseParser


SYSLOG_PATTERN = re.compile(
    r'(?P<ts>\w+\s+\d+\s+\d+:\d+:\d+)\s+'
    r'(?P<host>\S+)\s+'
    r'(?P<service>[a-zA-Z0-9_\-\/]+)'
    r'(?:\[(?P<pid>\d+)\])?:\s+'
    r'(?P<message>.*)'
)


class SyslogParser(BaseParser):

    def parse(self, line: str) -> Optional[Event]:

        match = SYSLOG_PATTERN.search(line)

        if not match:
            return None

        data = match.groupdict()

        ts = datetime.strptime(data["ts"], "%b %d %H:%M:%S")
        ts = ts.replace(year=datetime.now().year)

        pid = None
        if data["pid"]:
            pid = int(data["pid"])

        return Event(
            timestamp=ts,
            host=data["host"],
            service=data["service"],
            pid=pid,
            event_type="SYSLOG",
            message=data["message"],
            source_ip=None,
            severity="info"
        )
