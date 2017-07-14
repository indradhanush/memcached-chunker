"""
Memcache chunker
"""

# third party imports
from pymemcache.client.base import Client

# local imports
from chunker.exceptions import (
    SetFileFailed
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

    def set_file(self, key, file_path):
        with open(file_path, 'r') as f:
            data = f.readlines()

        file_string = ''.join(data)
        self._set_chunks(key, file_string)

    def _set_chunks(self, key_prefix, data):
        index = 0
        low = 0

        while low <= len(data):
            key = '{prefix}-{index}'.format(prefix=key_prefix, index=index)
            if self.client.set(key, data[low:low+self.chunk_size]) is False:
                raise SetFileFailed

            low += self.chunk_size
            index += 1
