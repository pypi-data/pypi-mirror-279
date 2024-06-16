import os
import hmac
import hashlib
import requests
import datetime
from enum import Enum
from base64 import b64encode
from typing import Dict, Mapping, Optional, NamedTuple, Sequence, Callable
from xml.etree import ElementTree
from dataclasses import dataclass
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor

from send_s3.config import Config
from send_s3.common import URLParams, HTTPHeaders, HTTPPayload

S3ProgressCallback = Callable[[int, int], None]


@dataclass
class S3Request:
    region: str
    method: str
    host: str
    path: str
    params: URLParams
    headers: HTTPHeaders
    secret_id: str
    secret_key: str
    data: bytes

    def __post_init__(self):
        date = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
        self.datetime = date
        self.date = date[:8]
        self.method = self.method.upper()
        self.path = self.path if self.path.startswith('/') else f"/{self.path}"
        self.params = dict(sorted(self.params.items()))
        headers = dict(self.headers)
        headers.update({
            'Host': self.host,
            'x-amz-date': self.datetime
        })
        self.headers = dict(sorted({k.lower(): v for k, v in headers.items()}.items()))
        if self.data is None:
            self.payload_hash = 'UNSIGNED-PAYLOAD'
        else:
            self.payload_hash = self.sha256_hex(self.data)

    @staticmethod
    def from_config(method: str, path: str, config: Config,
                    *headers_list: HTTPHeaders,
                    params: Optional[URLParams] = None,
                    data: Optional[HTTPPayload] = None) -> 'S3Request':
        headers: Dict[str, str] = {}
        for headers in headers_list:
            headers.update(headers)
        return S3Request(
            region=config.region,
            method=method,
            host=config.preferred_upload_domain(),
            path=path,
            params=params or {},
            headers=headers,
            secret_id=config.credentials.secret_id,
            secret_key=config.credentials.secret_key,
            data=data.encode('utf-8') if isinstance(data, str) else data
        )

    @staticmethod
    def sha256(data: HTTPPayload) -> bytes:
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).digest()

    @staticmethod
    def sha256_hex(data: HTTPPayload) -> str:
        return S3Request.sha256(data).hex()

    @staticmethod
    def hmac_sha256(key: HTTPPayload, msg: HTTPPayload) -> bytes:
        if isinstance(key, str):
            key = key.encode("utf-8")
        if isinstance(msg, str):
            msg = msg.encode("utf-8")
        return hmac.new(key, msg, hashlib.sha256).digest()

    @staticmethod
    def hmac_sha256_hex(key: HTTPPayload, msg: HTTPPayload) -> str:
        return S3Request.hmac_sha256(key, msg).hex()

    def url(self) -> str:
        return f"https://{self.host}{self.path}"

    def scope(self) -> str:
        return f"{self.date}/{self.region}/s3/aws4_request"

    def query_string(self) -> str:
        return urlencode(self.params)

    def header_signing_items(self) -> str:
        return '\n'.join([f"{k}:{v}" for k, v in self.headers.items()])

    def header_signing_keys(self) -> str:
        return ';'.join(self.headers.keys())

    def canonical_request(self) -> str:
        return "\n".join([
            self.method,
            self.path,
            self.query_string(),
            self.header_signing_items(),
            '',
            self.header_signing_keys(),
            self.payload_hash
        ])

    def signing_string(self) -> str:
        canonical_request = self.canonical_request()
        return "\n".join([
            'AWS4-HMAC-SHA256',
            self.datetime,
            self.scope(),
            self.sha256_hex(canonical_request)
        ])

    def signature(self) -> str:
        signing_string = self.signing_string()
        k_date = self.hmac_sha256(f"AWS4{self.secret_key}", self.date)
        k_region = self.hmac_sha256(k_date, self.region)
        k_service = self.hmac_sha256(k_region, 's3')
        k_signing = self.hmac_sha256(k_service, 'aws4_request')
        signature = self.hmac_sha256(k_signing, signing_string)
        return f"AWS4-HMAC-SHA256 Credential={self.secret_id}/{self.scope()}, " \
               f"SignedHeaders={self.header_signing_keys()}, Signature={signature.hex()}"

    def signed_headers(self) -> HTTPHeaders:
        result = dict(self.headers).copy()
        result['authorization'] = self.signature()
        result['x-amz-content-sha256'] = self.payload_hash
        return result

    def to_request(self) -> Mapping[str, str]:
        return {
            'method': self.method,
            'url': self.url(),
            'headers': self.signed_headers(),
            'params': self.params,
            'data': self.data,
        }


class S3MultipartUploadState(Enum):
    BEFORE_INITIATE = 0
    INITIALIZED = 1
    PARTS_UPLOADING = 2
    PENDING_FINALIZATION = 3
    FINISHED = 4


class S3MultipartSlice(NamedTuple):
    part_number: int
    start: int
    end: int


class S3MultipartResult(NamedTuple):
    part_number: int
    etag: str


class S3MultipartUpload:
    def __init__(self, config: Config, filepath: str, key: str, hashes: HTTPHeaders, headers: HTTPHeaders,
                 multipart_chunk_size: int = 1024 * 1024 * 5, multipart_threads: int = 8,
                 progress_callback: Optional[S3ProgressCallback] = None):
        self.config = config
        self.filepath = filepath
        self.key = key
        self.size = os.path.getsize(filepath)
        self.hashes = hashes
        self.headers = headers
        self.multipart_chunk_size = multipart_chunk_size
        self.multipart_threads = multipart_threads
        self.progress_callback = progress_callback
        self.upload_id: Optional[str] = None
        self.parts: Optional[Sequence[S3MultipartResult]] = None
        self.finalize_headers: Optional[HTTPHeaders] = None
        self.state = S3MultipartUploadState.BEFORE_INITIATE
        self.completed_bytes = 0

    def complete_bytes_and_progress_callback(self, increase_size: int = 0):
        self.completed_bytes += increase_size
        if self.progress_callback:
            self.progress_callback(self.completed_bytes, self.size)

    def initialize(self) -> None:
        assert self.state == S3MultipartUploadState.BEFORE_INITIATE
        headers = [self.headers, self.config.format_metadata(self.hashes)]
        signed_request = S3Request.from_config('POST', self.key, self.config,
                                               *headers, params={'uploads': ''})
        response = requests.request(**signed_request.to_request())
        response.raise_for_status()
        result = ElementTree.fromstring(response.text)
        self.state = S3MultipartUploadState.INITIALIZED
        self.upload_id = result.find('{*}UploadId').text

    def split_parts(self) -> Sequence[S3MultipartSlice]:
        for i, start in enumerate(range(0, self.size, self.multipart_chunk_size)):
            yield i + 1, start, min(start + self.multipart_chunk_size - 1, self.size)

    def upload_part(self, part_slice: S3MultipartSlice) -> S3MultipartResult:
        part_number, start, end = part_slice
        with open(self.filepath, 'rb') as f:
            f.seek(start)
            data = f.read(end - start + 1)
            headers = [self.headers, {
                'Content-MD5': b64encode(hashlib.md5(data).digest()).decode(),
                'X-Amz-Content-Sha256': hashlib.sha256(data).hexdigest(),
            }]
            signed_request = S3Request.from_config('PUT', self.key, self.config,
                                                   *headers, data=data,
                                                   params={'partNumber': part_number, 'uploadId': self.upload_id})
            response = requests.request(**signed_request.to_request())
            response.raise_for_status()
            self.complete_bytes_and_progress_callback(len(data))
            return S3MultipartResult(part_number, response.headers['ETag'])

    def upload_multipart(self) -> None:
        assert self.state == S3MultipartUploadState.INITIALIZED
        self.state = S3MultipartUploadState.PARTS_UPLOADING
        self.complete_bytes_and_progress_callback(0)
        with ThreadPoolExecutor(max_workers=self.multipart_threads) as executor:
            results = []
            for i, s, e in self.split_parts():
                thread = executor.submit(lambda: self.upload_part(S3MultipartSlice(i, s, e)))
                results.append(thread)
        self.parts = [r.result() for r in results]
        self.state = S3MultipartUploadState.PENDING_FINALIZATION

    def make_finalize_request_body(self) -> bytes:
        assert self.parts is not None
        parts_xml = ''.join([f'<Part><PartNumber>{p}</PartNumber><ETag>{e}</ETag></Part>' for p, e in self.parts])
        return f'<CompleteMultipartUpload>{parts_xml}</CompleteMultipartUpload>'.encode('utf-8')

    def finalize(self) -> None:
        assert self.state == S3MultipartUploadState.PENDING_FINALIZATION
        assert self.upload_id is not None
        signed_request = S3Request.from_config('POST', self.key, self.config,
                                               self.headers, data=self.make_finalize_request_body(),
                                               params={'uploadId': self.upload_id})
        response = requests.request(**signed_request.to_request())
        response.raise_for_status()
        self.finalize_headers = dict(response.headers)
        self.state = S3MultipartUploadState.FINISHED

    def __call__(self) -> 'S3MultipartUpload':
        self.initialize()
        self.upload_multipart()
        self.finalize()
        return self


__all__ = [
    "S3Request", "S3ProgressCallback",
    "S3MultipartUploadState", "S3MultipartSlice", "S3MultipartResult", "S3MultipartUpload"
]
