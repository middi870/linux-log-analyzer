import yaml
from collections import defaultdict, deque
from datetime import timedelta
from analyzer.event import Event


class RuleEngine:
    """
    Generic rule-based detection engine.
    Rules are loaded from YAML files.
    """

    def __init__(self, rule_file: str):

        with open(rule_file, "r") as f:
            self.rules = yaml.safe_load(f)

        self.windows = defaultdict(lambda: defaultdict(deque))

    def process(self, event: Event):

        alerts = []

        for rule_name, rule in self.rules.items():

            if event.event_type != rule["event_type"]:
                continue

            ip = event.source_ip
            threshold = rule["threshold"]
            window = timedelta(seconds=rule["window"])

            dq = self.windows[rule_name][ip]

            dq.append(event.timestamp)

            while dq and (event.timestamp - dq[0]) > window:
                dq.popleft()

            if len(dq) >= threshold:

                alerts.append({
                    "rule": rule_name,
                    "ip": ip,
                    "attempts": len(dq),
                    "window": rule["window"],
                    "message": rule["alert"]
                })

        return alerts
