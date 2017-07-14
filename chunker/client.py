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
    FileNotFound,
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

    def set_file(self, key, file_path):
        with open(file_path, 'r') as f:
            data = f.readlines()

        file_string = ''.join(data)
        self._set_chunks(key, file_string)

    def _set_chunks(self, key_prefix, data):
        index = 0
        low = 0

        hashes = []

        while low <= len(data):
            key = self._get_key(key_prefix, index)
            chunk = data[low:low+self.chunk_size]

            chunk_hash = hashlib.pbkdf2_hmac('sha1', chunk, '', 80)
            hashes.append(binascii.hexlify(chunk_hash))

            if self.client.set(key, chunk) is False:
                raise SetFileFailed

            low += self.chunk_size
            index += 1

        self._set_metadata(key_prefix, ','.join(hashes))

    def _set_metadata(self, key_prefix, metadata):
        key = self._get_key(key_prefix, 'metadata')

        if self.client.set(key, metadata) is False:
            raise SetMetadataFailed

    def get_file(self, key, file_path):
        chunks = self._get_chunks(key)
        if not chunks:
            raise FileNotFound

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
