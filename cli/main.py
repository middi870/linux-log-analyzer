import argparse

from reader.file_reader import FileReader
from reader.stream_reader import StreamReader
from reader.directory_reader import DirectoryReader
from reader.journal_reader import JournalReader

from parser.auth_parser import AuthLogParser
from parser.nginx_parser import NginxParser
from parser.syslog_parser import SyslogParser

from analyzer.rule_engine import RuleEngine
from analyzer.statistics import Statistics
from analyzer.dashboard import Dashboard


def process_line(parsers, engine, stats, line):

    event = None

    for parser in parsers:
        event = parser.parse(line)
        if event:
            break

    if not event:
        return

    stats.process(event)

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

    stats = Statistics()

    arg_parser = argparse.ArgumentParser(
        description="Linux Log Analyzer"
    )

    arg_parser.add_argument("--file", help="Analyze single log file")
    arg_parser.add_argument("--dir", help="Analyze directory of log files")
    arg_parser.add_argument("--follow", help="Follow log file in real-time")
    arg_parser.add_argument("--journal", help="Read logs from systemd journal")
    arg_parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Enable live terminal dashboard"
    )

    args = arg_parser.parse_args()

    parsers = [
        AuthLogParser(),
        NginxParser(),
        SyslogParser()
    ]

    engine = RuleEngine("rules/rules.yaml")

    dashboard = None

    if args.dashboard:
        dashboard = Dashboard(stats)
        dashboard.start()

    try:

        if args.file:

            reader = FileReader(args.file)

            for line in reader.read_lines():
                process_line(parsers, engine, stats, line)

            if not args.dashboard:
                stats.report()

        elif args.dir:

            reader = DirectoryReader(args.dir)

            for line in reader.read_lines():
                process_line(parsers, engine, stats, line)

            if not args.dashboard:
                stats.report()

        elif args.follow:

            reader = StreamReader(args.follow)

            for line in reader.follow():
                process_line(parsers, engine, stats, line)

        elif args.journal:

            reader = JournalReader(args.journal)

            for line in reader.read_lines():
                process_line(parsers, engine, stats, line)

            if not args.dashboard:
                stats.report()

        else:
            arg_parser.print_help()

    except KeyboardInterrupt:

        print("\nStopping analyzer...")

    finally:

        if dashboard:
            dashboard.stop()


if __name__ == "__main__":
    main()
