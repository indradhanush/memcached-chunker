"""
Exceptions for Memcached chunker
"""


class SetMetadataFailed(Exception):
    pass


class SetFileFailed(Exception):
    pass


class FileNotFound(Exception):
    pass
