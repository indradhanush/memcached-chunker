"""
Exceptions for Memcached chunker
"""


class SetMetadataFailed(Exception):
    pass


class SetFileFailed(Exception):
    pass


class FileNotFound(Exception):
    pass


class FileCorrupted(Exception):
    pass


class MetadataNotAvailable(Exception):
    pass
