"""
Memcache chunker
"""

# system imports
from collections import OrderedDict

# third party imports
from pymemcache.client.base import Client

# local imports
from chunker.exceptions import (
    SetMetadataFailed,
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

    def set_file(self, key, file_obj):
        with open(file_obj, 'r') as f:
            data = f.readlines()

        file_string = ''.join(data)
        chunks = self._get_chunks(key, file_string)

        self._set_metadata(key, chunks.keys())

        for key, value in chunks.items():
            if self.client.set(key, value) is False:
                raise SetFileFailed

    def _get_chunks(self, key_prefix, data):
        chunks = OrderedDict()

        index = 0
        low = 0
        while low <= len(data):
            chunk = data[low:low+self.chunk_size]

            key = '{prefix}-{index}'.format(prefix=key_prefix, index=index)

            chunks[key] = chunk

            low += self.chunk_size
            index += 1

        return chunks

    def _set_metadata(self, key, meta_data):
        key = '{name}-metadata'.format(name=key)
        if self.client.set(key, ','.join(meta_data)) is False:
            raise SetMetadataFailed
