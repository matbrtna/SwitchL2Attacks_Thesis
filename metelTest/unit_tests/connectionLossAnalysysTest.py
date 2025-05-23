import unittest
import sys

# setting path


# importing
sys.path.append(".")

from connectionLossAnalysys import getNonZeroValues, sumarizeValues,convertToMS

# using

class TestMainFunctions(unittest.TestCase):

    def test_getNonZeroValues(self):
        self.assertEqual(getNonZeroValues([0, 1, 2, 0, 3]), [1, 2, 3])
        self.assertEqual(getNonZeroValues([0, 0, 0]), [])
        self.assertEqual(getNonZeroValues([5, 6]), [5, 6])

    def test_sumarizeValues(self):
        self.assertEqual(sumarizeValues([1, 2, 3]), 6)
        self.assertEqual(sumarizeValues([]), 0)

    def test_convertToMS(self):
        self.assertEqual(convertToMS(5), 50)
        self.assertEqual(convertToMS(0), 0)

    def test_convertToMS_with_float(self):
        self.assertAlmostEqual(convertToMS(2.5), 25.0)

if __name__ == "__main__":
    unittest.main()