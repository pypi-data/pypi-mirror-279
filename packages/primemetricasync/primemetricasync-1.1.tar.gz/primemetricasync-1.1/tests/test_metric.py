# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from src.metric.metric import get_metric


class TestSimple(unittest.TestCase):

    def test_metric(self):
        self.assertEqual(get_metric(3,4), 5)


if __name__ == '__main__':
    unittest.main()
