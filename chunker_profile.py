# System imports
from memory_profiler import profile
import os

# Local imports
from chunker.client import Chunker


@profile
def run_profile_test(file_path, chunk_size):
    chunker = Chunker('localhost', 11211, chunk_size)
    chunker.set_file('profiler', file_path)
    chunker.get_file('profiler', 'test_file')
    os.remove('test_file')


if __name__ == '__main__':
    chunk_size = 1000 ** 2

    file_path = 'chunker/test_file.txt'

    # pr = cProfile.Profile()
    # pr.enable()

    run_profile_test(file_path, chunk_size)

    # pr.disable()

    # s = StringIO.StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print s.getvalue()
