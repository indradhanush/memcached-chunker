"""
Tests for Memcache chunker
"""

from unittest.case import TestCase

from chunker.client import Chunker


class ChunkerTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.chunker = Chunker('localhost', 11211, 10)
        cls.test_string = 'aaaaaaaaaabbbbbbbbbbccccccccccdddddd'

    def test__set_chunks(self):
        self.chunker._set_chunks('test', self.test_string)

        self.assertEqual(self.chunker.client.get('test-0'), 'aaaaaaaaaa')
        self.assertEqual(self.chunker.client.get('test-1'), 'bbbbbbbbbb')
        self.assertEqual(self.chunker.client.get('test-2'), 'cccccccccc')
        self.assertEqual(self.chunker.client.get('test-3'), 'dddddd')
