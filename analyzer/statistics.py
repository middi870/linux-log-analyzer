from collections import defaultdict, Counter
from analyzer.event import Event


class Statistics:
    """
    Real-time analytics module.

    Tracks:
    - total events
    - event type counts
    - top source IPs
    """

    def __init__(self):

        self.total_events = 0
        self.event_counts = Counter()
        self.ip_counts = defaultdict(int)

    def process(self, event: Event):

        self.total_events += 1
        self.event_counts[event.event_type] += 1

        if event.source_ip:
            self.ip_counts[event.source_ip] += 1

    def report(self, top_n=5):

        print("\n===== Log Analysis Summary =====\n")

        print(f"Total Events: {self.total_events}\n")

        print("Event Types")
        print("-------------------")
        for event, count in self.event_counts.items():
            print(f"{event:<15} {count}")

        print("\nTop Source IPs")
        print("-------------------")

        sorted_ips = sorted(
            self.ip_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for ip, count in sorted_ips[:top_n]:
            print(f"{ip:<15} {count}")

        print("\n===============================\n")
