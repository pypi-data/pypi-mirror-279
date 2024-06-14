import unittest
import numpy as np


class EarthTwoBodyTests(unittest.TestCase):

    def test_simple(self):
        self.assertTrue(True)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(EarthTwoBodyTests))
    return test_suite


if __name__ == "__main__":
    unittest.main()
