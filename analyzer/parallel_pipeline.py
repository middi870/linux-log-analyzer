from concurrent.futures import ThreadPoolExecutor
from typing import List

from analyzer.event import Event


class ParallelPipeline:
    """
    Parallel log processing pipeline using worker threads.
    """

    def __init__(self, parsers, engine, stats, workers=4):

        self.parsers = parsers
        self.engine = engine
        self.stats = stats
        self.workers = workers

        self.executor = ThreadPoolExecutor(max_workers=workers)

    def process_line(self, line):

        event = None

        for parser in self.parsers:
            event = parser.parse(line)
            if event:
                break

        if not event:
            return

        self.stats.process(event)

        alerts = self.engine.process(event)

        for alert in alerts:
            print(
                f"\n[ALERT] {alert['message']}\n"
                f"Rule: {alert['rule']}\n"
                f"IP: {alert['ip']}\n"
                f"Attempts: {alert['attempts']}\n"
                f"Window: {alert['window']} seconds\n"
            )

    def submit(self, line):
        self.executor.submit(self.process_line, line)

    def shutdown(self):
        self.executor.shutdown(wait=True)
