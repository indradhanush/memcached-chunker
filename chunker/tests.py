"""
Tests for Memcache chunker
"""

# System imports
import binascii
import hashlib
import os
import tempfile
from unittest.case import TestCase

# Local imports
from chunker.client import Chunker


class ChunkerTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.chunker = Chunker('localhost', 11211, 10)
        cls.test_string = 'aaaaaaaaaabbbbbbbbbbccccccccccdddddd'
        cls.hashes = [
            binascii.hexlify(
                hashlib.pbkdf2_hmac('sha1', 'aaaaaaaaaa', '', 80)
            ),
            binascii.hexlify(
                hashlib.pbkdf2_hmac('sha1', 'bbbbbbbbbb', '', 80)
            ),
            binascii.hexlify(
                hashlib.pbkdf2_hmac('sha1', 'cccccccccc', '', 80)
            ),
            binascii.hexlify(
                hashlib.pbkdf2_hmac('sha1', 'dddddd', '', 80)
            )
        ]

    def test__set_chunks(self):
        self.chunker._set_chunks('test', self.test_string)

        self.assertEqual(self.chunker.client.get('test-0'), 'aaaaaaaaaa')
        self.assertEqual(self.chunker.client.get('test-1'), 'bbbbbbbbbb')
        self.assertEqual(self.chunker.client.get('test-2'), 'cccccccccc')
        self.assertEqual(self.chunker.client.get('test-3'), 'dddddd')

    def test_set_file(self):
        with tempfile.NamedTemporaryFile() as f:
            f.write(self.test_string)
            f.flush()
            self.chunker.set_file('test', f.name)

        self.assertEqual(self.chunker.client.get('test-0'), 'aaaaaaaaaa')
        self.assertEqual(self.chunker.client.get('test-1'), 'bbbbbbbbbb')
        self.assertEqual(self.chunker.client.get('test-2'), 'cccccccccc')
        self.assertEqual(self.chunker.client.get('test-3'), 'dddddd')

        self.assertEqual(self.chunker.client.get('test-metadata'), ','.join(self.hashes))

    def test__get_chunks(self):
        with tempfile.NamedTemporaryFile() as f:
            f.write(self.test_string)
            f.flush()
            self.chunker.set_file('test', f.name)

        chunks = self.chunker._get_chunks('test')

        self.assertEqual(chunks[0], 'aaaaaaaaaa')
        self.assertEqual(chunks[1], 'bbbbbbbbbb')
        self.assertEqual(chunks[2], 'cccccccccc')
        self.assertEqual(chunks[3], 'dddddd')

    def test_get_file(self):
        with tempfile.NamedTemporaryFile() as f:
            f.write(self.test_string)
            f.flush()
            self.chunker.set_file('test', f.name)

        self.chunker.get_file('test', 'test_file')

        with open('test_file', 'r') as f:
            self.assertEqual(self.test_string, ''.join(f.readlines()))

        os.remove('test_file')
