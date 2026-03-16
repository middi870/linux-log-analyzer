from collections import defaultdict, deque
from datetime import timedelta
from analyzer.event import Event


class BruteForceDetector:
    """
    Detect SSH brute force attacks using a sliding time window.
    """

    def __init__(self, threshold: int = 5, window_seconds: int = 60):
        self.threshold = threshold
        self.window = timedelta(seconds=window_seconds)

        # store timestamps of failed logins per IP
        self.events = defaultdict(deque)

    def process(self, event: Event):

        if event.event_type != "AUTH_FAIL":
            return None

        ip = event.source_ip
        timestamp = event.timestamp

        dq = self.events[ip]
        dq.append(timestamp)

        # remove old events outside the time window
        while dq and (timestamp - dq[0]) > self.window:
            dq.popleft()

        if len(dq) >= self.threshold:
            return {
                "type": "BRUTE_FORCE",
                "ip": ip,
                "attempts": len(dq),
                "window": self.window.seconds,
            }

        return None
