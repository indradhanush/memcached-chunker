"""
Memcache chunker
"""

# System imports
import binascii
import hashlib

# third party imports
from pymemcache.client.base import Client

# local imports
from chunker.exceptions import (
    FileCorrupted,
    FileNotFound,
    MetadataNotAvailable,
    SetFileFailed,
    SetMetadataFailed
)


class Chunker(object):

    def __init__(self, address, port, chunk_size):
        self._client = None
        self.address = address
        self.port = port
        self.chunk_size = chunk_size

    @property
    def client(self):
        if self._client is None:
            self._client = Client((self.address, self.port))

        return self._client

    @staticmethod
    def _get_key(prefix, suffix):
        return '{prefix}-{suffix}'.format(prefix=prefix, suffix=suffix)

    @staticmethod
    def _get_chunk_hash(chunk):
        sha1_hash = hashlib.pbkdf2_hmac('sha1', chunk, '', 80)
        return binascii.hexlify(sha1_hash)

    def set_file(self, key_prefix, file_path):
        f = open(file_path, 'r')

        index = 0

        hashes = []

        while True:
            # TODO: handle when an entire chunk is not read
            data = f.read(self.chunk_size)

            if not data:
                break

            key = self._get_key(key_prefix, index)
            chunk = data

            hashes.append(self._get_chunk_hash(chunk))

            self._set_chunk(key, chunk)

            index += 1

        self._set_metadata(key_prefix, ','.join(hashes))

    def _set_chunk(self, key, data):
        if self.client.set(key, data) is False:
            raise SetFileFailed

    def _set_metadata(self, key_prefix, metadata):
        key = self._get_key(key_prefix, 'metadata')

        if self.client.set(key, metadata) is False:
            raise SetMetadataFailed

    def get_file(self, key, file_path):
        chunks = self._get_chunks(key)
        if not chunks:
            raise FileNotFound

        self._verify_metadata(key, chunks)
        with open(file_path, 'w') as f:
            f.write(''.join(chunks))

    def _get_chunks(self, key_prefix):
        index = 0
        chunks = []
        while True:
            key = self._get_key(key_prefix, index)
            data = self.client.get(key)
            if not data:
                break

            chunks.append(data)
            index += 1

        return chunks

    def _verify_metadata(self, key, chunks):
        metadata_key = self._get_key(key, 'metadata')
        hash_str = self.client.get(metadata_key)
        if hash_str is None:
            raise MetadataNotAvailable

        hashes = hash_str.split(',')
        if any(
                sha1_hash != self._get_chunk_hash(chunk)
                for sha1_hash, chunk in zip(hashes, chunks)
        ):
            raise FileCorrupted
