import os
import json
import sqlite3
from typing import Any, Dict, Optional, Sequence, NamedTuple, Literal, List
from datetime import datetime
from dataclasses import dataclass

from send_s3.common import app_directory, human_readable_size


class Database:
    def __init__(self):
        path = app_directory("log.sqlite3")
        schema_sql = os.path.join(os.path.dirname(__file__), "schema.sql")
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        with open(schema_sql, "r") as f:
            self.cursor.executescript(f.read())

    def insert(self, entry: 'LogEntry') -> Optional[int]:
        query = LogEntryQuery(self.cursor).insert(entry)
        query.execute()
        return query.cursor.lastrowid

    def select(self, options: 'LogEntrySelectOptions') -> Sequence['LogEntry']:
        query = LogEntryQuery(self.cursor).select()
        if options.time_from:
            query.where_gt('timestamp', int(options.time_from.timestamp()))
        if options.time_to:
            query.where_lt('timestamp', int(options.time_to.timestamp()))
        if options.name:
            query.where_like('filepath', options.name)
        query.order_by('timestamp', 'DESC')
        query.limit(options.limit).finish_select()
        query.execute()
        for row in query.cursor.fetchall():
            yield LogEntry(*row)

    def close(self):
        self.connection.close()

    def __del__(self):
        self.close()


class LogEntry(NamedTuple):
    timestamp: int
    filepath: str
    key: str
    size: int
    checksum: str
    url: str
    data: str

    @classmethod
    def sequence(cls) -> str:
        return ','.join(cls._fields)

    def display_size(self):
        return human_readable_size(self.size)

    def display_time(self):
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S %Z')

    def data_dict(self) -> Dict[str, Any]:
        return json.loads(self.data)


@dataclass
class LogEntrySelectOptions:
    limit: int
    time_from: Optional[datetime]
    time_to: Optional[datetime]
    name: Optional[str]


class LogEntryQuery:
    TABLE = 'logs'
    FIELDS = LogEntry.sequence()
    PLACEHOLDERS = ', '.join(['?' for _ in LogEntry._fields])

    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor
        self.sql = ''
        self.values: List[Any] = list()
        self.state = 'init'

    def execute(self):
        assert self.state == 'finished'
        if len(self.values) == 0:
            self.cursor.execute(self.sql)
        else:
            self.cursor.execute(self.sql, self.values)
        self.cursor.connection.commit()

    def insert(self, entry: LogEntry) -> 'LogEntryQuery':
        assert self.state == 'init'
        self.sql = f'INSERT INTO {self.TABLE} ({self.FIELDS}) VALUES ({self.PLACEHOLDERS})'
        self.values = list(entry)
        self.state = 'finished'
        return self

    def select(self) -> 'LogEntryQuery':
        assert self.state == 'init'
        self.sql = f'SELECT {self.FIELDS} FROM {self.TABLE} WHERE 1=1 '
        self.state = 'select'
        return self

    def where_lt(self, column: str, value: Any) -> 'LogEntryQuery':
        assert self.state == 'select'
        self.sql += f' AND {column} < ? '
        self.values.append(value)
        return self

    def where_gt(self, column: str, value: Any) -> 'LogEntryQuery':
        assert self.state == 'select'
        self.sql += f' AND {column} > ? '
        self.values.append(value)
        return self

    def where_like(self, column: str, value: Any) -> 'LogEntryQuery':
        assert self.state == 'select'
        self.sql += f' AND {column} LIKE ? '
        self.values.append(f'%{value}%')
        return self

    def limit(self, limit: int) -> 'LogEntryQuery':
        assert self.state == 'select'
        self.sql += f' LIMIT ?'
        self.values.append(limit)
        return self

    def order_by(self, column: str, order: Literal['ASC', 'DESC']) -> 'LogEntryQuery':
        assert self.state == 'select'
        assert order in ('ASC', 'DESC')
        assert column in self.FIELDS
        self.sql += f' ORDER BY {column} {order}'
        return self

    def finish_select(self) -> 'LogEntryQuery':
        assert self.state == 'select'
        self.state = 'finished'
        return self


__all__ = ['Database', 'LogEntry', 'LogEntrySelectOptions']
