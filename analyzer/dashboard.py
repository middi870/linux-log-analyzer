import time
import os
import threading


class Dashboard:
    """
    Live terminal dashboard displaying statistics in real time.
    """

    def __init__(self, stats, interval=1):
        self.stats = stats
        self.interval = interval
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join()

    def run(self):

        while self.running:

            os.system("clear")

            print("===== Live Log Analyzer Dashboard =====\n")

            print(f"Total Events: {self.stats.total_events}\n")

            print("Event Types")
            print("-------------------")

            for event, count in self.stats.event_counts.items():
                print(f"{event:<15} {count}")

            print("\nTop Source IPs")
            print("-------------------")

            sorted_ips = sorted(
                self.stats.ip_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )

            for ip, count in sorted_ips[:5]:
                print(f"{ip:<15} {count}")

            print("\nPress Ctrl+C to stop")

            time.sleep(self.interval)
