import os
import sys
import time
import json
import hashlib
import argparse
import traceback
import urllib.parse
from typing import Mapping, Tuple, Optional

from send_s3.db import Database, LogEntry
from send_s3.s3 import S3MultipartUpload
from send_s3.config import Config
from send_s3.common import PROG, VERSION, LINESEP, Console, HTTPHeaders, human_readable_size

MultiPartSlice = Tuple[int, int, int]
MultiPartResult = Tuple[int, str]


class File:
    def __init__(self, args: argparse.Namespace, config: Config, filepath: str,
                 checksum_chunk_size: int = 1024 * 1024 * 16):
        if not self.check(filepath):
            raise Exception(f"Can not upload file: '{filepath}'")
        self.args = args
        self.config = config
        self.filepath = filepath
        self.key = config.format_filename(filepath)
        self.url_encoded_key = urllib.parse.quote(self.key)
        self.checksum_chunk_size = checksum_chunk_size
        self.hide_progress = self.args.typora
        self.show_single_download_link = self.args.typora
        # self.headers: HTTPHeaders = {
        #     'User-Agent': f'{PROG}/{VERSION}',
        # }

    def __call__(self, *args, **kwargs):
        self.upload_file()

    @staticmethod
    def check(filepath: str) -> bool:
        if not (os.path.exists(filepath)):
            Console() >> f"ERROR: File Not Found: {filepath}" >> LINESEP >> sys.stderr
            return False
        if os.path.isdir(filepath):
            Console() >> f"ERROR: Is a directory: {filepath}" >> LINESEP >> sys.stderr
            return False
        return True

    def hash(self) -> HTTPHeaders:
        available_checksums = list(filter(lambda x: hasattr(hashlib, x), self.config.checksum))
        available_checksums.append('sha256')
        hash_list = {}
        for checksum in set(available_checksums):
            hash_list[checksum] = getattr(hashlib, checksum)()
        with open(self.filepath, 'rb') as f:
            while chunk := f.read(self.checksum_chunk_size):
                for hash_func in hash_list.values():
                    hash_func.update(chunk)
        return {k: v.hexdigest() for k, v in hash_list.items()}

    def progress_callback(self, completed: int, total: int) -> None:
        if self.hide_progress:
            return
        display_completed = human_readable_size(min(completed, total))
        display_total = human_readable_size(total)
        percentage = (completed / total) * 100
        Console() >> f"{percentage:.2f}% ({display_completed} / {display_total}) [{self.key}]\r" >> sys.stderr

    def progress_complete(self) -> None:
        if not self.hide_progress:
            Console() >> LINESEP >> sys.stderr

    def download_link(self, domain: Optional[str] = None) -> str:
        if not domain:
            domain = self.config.preferred_download_domain()
        return f"https://{domain}/{self.url_encoded_key}"

    def download_links(self) -> Mapping[str, str]:
        return {
            domain_type: self.download_link(domain)
            for domain_type, domain in self.config.preferred_download_domains().items()
        }

    def write_upload_log(self, hashes: HTTPHeaders, upload_result: S3MultipartUpload) -> None:
        db = Database()
        db.insert(LogEntry(
            timestamp=int(time.time()),
            filepath=self.filepath,
            key=self.key,
            size=os.path.getsize(self.filepath),
            checksum=f"sha256:{hashes['sha256']}",
            url=self.download_link(),
            data=json.dumps({
                'parts': upload_result.parts,
                'upload_id': upload_result.upload_id,
                'headers': upload_result.finalize_headers,
                'download_links': self.download_links()})))

    def show_download_links(self) -> None:
        if self.show_single_download_link:
            Console() >> self.download_link() >> LINESEP >> sys.stdout
            return
        links = self.download_links()
        length = max(max(map(len, links.keys())), len('file')) + 2
        Console() >> f"{'local':<{length}}: {self.filepath}" >> LINESEP >> sys.stdout
        for domain_type, url in links.items():
            Console() >> f"{domain_type:<{length}}: {url}" >> LINESEP >> sys.stdout

    def upload_file(self):
        hashes = self.hash()
        result = S3MultipartUpload(
            self.config,
            filepath=self.filepath,
            key=self.url_encoded_key,
            headers={'User-Agent': f'{PROG}/{VERSION}'},
            hashes=hashes,
            progress_callback=lambda x, y: self.progress_callback(x, y),
        )()
        self.progress_complete()
        self.write_upload_log(hashes, result)
        self.show_download_links()


def main(args: argparse.Namespace) -> int:
    pause_after_execution = args.windows_sendto
    quiet_output = args.typora
    config = Config.load()
    for file in args.files:
        # noinspection PyBroadException
        try:
            File(args, config, file)()
        except Exception as e:
            Console() >> f"ERROR: {e}" >> LINESEP >> sys.stderr
            Console() >> traceback.format_exc() >> LINESEP >> sys.stderr
            continue
        finally:
            if not quiet_output:
                Console() >> ("-" * 60) >> LINESEP >> sys.stdout
    if pause_after_execution:
        input('Done! Press Enter to close this window...')
    return 0


def register_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("files", metavar="FILE", type=str, nargs="+", help="Files to upload")
    parser.add_argument("--typora", dest="typora", action="store_true")
    parser.add_argument("--windows-sendto", dest="windows_sendto", action="store_true")


__all__ = ['main', 'register_arguments']
