import argparse

from reader.file_reader import FileReader
from reader.stream_reader import StreamReader
from parser.auth_parser import AuthLogParser
from analyzer.rule_engine import RuleEngine


def process_line(parser, engine, line):

    event = parser.parse(line)

    if not event:
        return

    print(
        f"[{event.event_type}] "
        f"{event.timestamp} "
        f"{event.source_ip}"
    )

    alerts = engine.process(event)

    for alert in alerts:
        print(
            f"\n[ALERT] {alert['message']}\n"
            f"Rule: {alert['rule']}\n"
            f"IP: {alert['ip']}\n"
            f"Attempts: {alert['attempts']}\n"
            f"Window: {alert['window']} seconds\n"
        )


def main():

    parser = argparse.ArgumentParser(
        description="Linux Log Analyzer"
    )

    parser.add_argument("--file", help="Path to log file")
    parser.add_argument("--follow", help="Follow log file")

    args = parser.parse_args()

    log_parser = AuthLogParser()
    engine = RuleEngine("rules/ssh_rules.yaml")

    if args.file:

        reader = FileReader(args.file)

        for line in reader.read_lines():
            process_line(log_parser, engine, line)

    elif args.follow:

        reader = StreamReader(args.follow)

        for line in reader.follow():
            process_line(log_parser, engine, line)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
