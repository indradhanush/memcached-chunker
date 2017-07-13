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

    def test__get_chunk(self):
        chunks = self.chunker._get_chunks('test', self.test_string)

        self.assertEqual(len(chunks.keys()), 4)
        self.assertEqual(chunks['test-0'], 'aaaaaaaaaa')
        self.assertEqual(chunks['test-1'], 'bbbbbbbbbb')
        self.assertEqual(chunks['test-2'], 'cccccccccc')
        self.assertEqual(chunks['test-3'], 'dddddd')

    def test__set_metadata(self):
        chunks = self.chunker._get_chunks('test', self.test_string)

        self.chunker._set_metadata('test', chunks)

        metadata = self.chunker.client.get('test-metadata')
        self.assertEqual(metadata, 'test-0,test-1,test-2,test-3')
