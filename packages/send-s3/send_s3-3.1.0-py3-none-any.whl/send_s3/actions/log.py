import re
import sys
import json
import datetime
import argparse
from typing import Union, Optional

from send_s3.db import Database, LogEntrySelectOptions, LogEntry
from send_s3.common import LINESEP, Console

DATE_REGEX = r'^\d{4}-\d{2}-\d{2}$'
TIME_REGEX = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'


def parse_time(time_expr: Optional[str]) -> Union[None, False, datetime.datetime]:
    if time_expr is None:
        return None
    if re.match(DATE_REGEX, time_expr):
        time_expr += 'T00:00:00'
    if not re.match(TIME_REGEX, time_expr):
        Console() >> f"ERROR: Invalid time format: {time_expr}" >> LINESEP >> sys.stderr
        raise False
    try:
        return datetime.datetime.strptime(time_expr, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        Console() >> f"ERROR: Invalid time format: {time_expr}" >> LINESEP >> sys.stderr
        raise False


def print_log(log: LogEntry) -> None:
    Console() >> "\033[1;32m" >> log.checksum >> "\033[0m" >> LINESEP >> sys.stdout
    Console() >> "\033[1;33m" >> f"Date: \033[0m{log.display_time()}" >> LINESEP >> sys.stdout
    Console() >> "\033[1;33m" >> f"File: \033[0m{log.filepath}" >> LINESEP >> sys.stdout
    Console() >> "\033[1;33m" >> f"Key:  \033[0m{log.key}" >> LINESEP >> sys.stdout
    Console() >> "\033[1;33m" >> f"Size: \033[0m{log.display_size()}" >> LINESEP >> sys.stdout
    Console() >> "\033[1;33m" >> f"URL:  \033[0m{log.url}" >> LINESEP >> sys.stdout
    Console() >> LINESEP >> sys.stdout
    print_download_links(log)
    Console() >> LINESEP >> ("-" * 60) >> LINESEP >> sys.stdout


def print_download_links(log: LogEntry) -> None:
    download_links = log.data_dict().get('download_links', {})
    max_len = max(map(len, download_links.keys()))
    Console() >> '  Alternative Download Links:' >> LINESEP >> sys.stdout
    for domain, url in download_links.items():
        Console() >> '    ' >> f"{domain:<{max_len}}: {url}" >> LINESEP >> sys.stdout


def main(args: argparse.Namespace) -> int:
    db = Database()
    time_from, time_to = parse_time(args.time_from), parse_time(args.time_to)
    if time_from is False or time_to is False:
        return 1
    logs = db.select(LogEntrySelectOptions(limit=args.limit or 100, name=args.name,
                                           time_from=time_from, time_to=time_to))
    if args.json:
        Console() >> json.dumps(logs, indent=2, ensure_ascii=False) >> sys.stdout
        return 0
    for log in logs:
        print_log(log)
    return 0


def register_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('-f', '--from', dest='time_from',
                        help='Time from, format: "Y-m-d" or "Y-m-dTH:M:S"', required=False, default=None)
    parser.add_argument('-t', '--to', dest='time_to',
                        help='Time to, format: "Y-m-d" or "Y-m-dTH:M:S"', required=False, default=None)
    parser.add_argument('-n', '--name', dest='name',
                        help='Keyword of name (or path) of original file to search', required=False, default=None)
    parser.add_argument('-l', '--limit', dest='limit',
                        help='Limit the number of logs to show', required=False, default=100, type=int)
    parser.add_argument('--json', dest='json', action='store_true', help='Output in JSON format')


__all__ = ['main', 'register_arguments']
