
import unittest
import sys

sys.path.append(".")
from connectionThrottling import getSpeedList, getAvarage, convertToMb, getMax, evaulateTest

class TestConnectionThrottling(unittest.TestCase):

    def setUp(self):
        self.test_data = {
            "intervals": [
                {"sum": {"bits_per_second": 80000000}},
                {"sum": {"bits_per_second": 90000000}},
                {"sum": {"bits_per_second": 100000000}},
            ]
        }

    def test_getSpeedList(self):
        self.assertEqual(getSpeedList(self.test_data), [80000000, 90000000, 100000000])

    def test_getAvarage(self):
        self.assertEqual(getAvarage([10, 20, 30]), 20)
        self.assertEqual(getAvarage([0, 0]), 0)

    def test_getMax(self):
        self.assertEqual(getMax([10, 20, 30]), 30)
        self.assertEqual(getMax([100]), 100)

    def test_convertToMb(self):
        self.assertEqual(convertToMb(1000000), 1.0)
        self.assertAlmostEqual(convertToMb(85000000), 85.0)




if __name__ == "__main__":
    unittest.main()