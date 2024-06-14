import unittest
from time import time

from utils import build_test_params
from tiktok_simple_scraper.x_bogus import XBogus


class TestXBogus(unittest.TestCase):

    def test_get_x_bogus(self):
        expected_x_bogus = 'DFSzswVuAoTANjM/tA8dxNzDOl8x'
        fixed_time = 1717028537
        params = build_test_params(fixed_time)
        xbogus = XBogus()
        result = xbogus.get_x_bogus(query=params, time_to_take=fixed_time)
        self.assertEqual(expected_x_bogus, result)
