import unittest

import sys


# setting path


# importing
sys.path.append(".")
from connectionSpeed import getSpeedList, getAvarage, getMax, convertToMb


class TestConnectionSpeed(unittest.TestCase):

    def test_getSpeedList(self):
        test_data = {
            "intervals": [
                {"sum": {"bits_per_second": 100000000}},
                {"sum": {"bits_per_second": 90000000}},
                {"sum": {"bits_per_second": 95000000}},
            ]
        }
        expected = [100000000, 90000000, 95000000]
        self.assertEqual(getSpeedList(test_data), expected)

    def test_getAvarage(self):
        self.assertEqual(getAvarage([100, 200, 300]), 200)
        self.assertEqual(getAvarage([0, 0, 0]), 0)

    def test_getMax(self):
        self.assertEqual(getMax([100, 200, 300]), 300)
        self.assertEqual(getMax([1]), 1)

    def test_convertToMb(self):
        self.assertEqual(convertToMb(1000000), 1.0)
        self.assertEqual(convertToMb(0), 0.0)
        self.assertAlmostEqual(convertToMb(125000000), 125)




if __name__ == "__main__":
    unittest.main()