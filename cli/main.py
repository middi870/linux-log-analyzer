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
from analyzer.parallel_pipeline import ParallelPipeline


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

    arg_parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel processing workers"
    )

    args = arg_parser.parse_args()

    parsers = [
        AuthLogParser(),
        NginxParser(),
        SyslogParser()
    ]

    engine = RuleEngine("rules/rules.yaml")

    pipeline = ParallelPipeline(
        parsers=parsers,
        engine=engine,
        stats=stats,
        workers=args.workers
    )

    dashboard = None

    if args.dashboard:
        dashboard = Dashboard(stats)
        dashboard.start()

    try:

        if args.file:

            reader = FileReader(args.file)

            for line in reader.read_lines():
                pipeline.submit(line)

            pipeline.shutdown()

            if not args.dashboard:
                stats.report()

        elif args.dir:

            reader = DirectoryReader(args.dir)

            for line in reader.read_lines():
                pipeline.submit(line)

            pipeline.shutdown()

            if not args.dashboard:
                stats.report()

        elif args.follow:

            reader = StreamReader(args.follow)

            for line in reader.follow():
                pipeline.submit(line)

        elif args.journal:

            reader = JournalReader(args.journal)

            for line in reader.read_lines():
                pipeline.submit(line)

            pipeline.shutdown()

            if not args.dashboard:
                stats.report()

        else:
            arg_parser.print_help()

    except KeyboardInterrupt:

        print("\nStopping analyzer...")

    finally:

        if dashboard:
            dashboard.stop()

        pipeline.shutdown()


if __name__ == "__main__":
    main()
