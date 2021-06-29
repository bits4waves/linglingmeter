import unittest
import main
import logging


def setUpModule():
    """Disable logging while doing these tests."""
    logging.disable()


def tearDownModule():
    """Re-enable logging after doing these tests."""
    logging.disable(logging.NOTSET)


class TestMain(unittest.TestCase):

    def test_create_threshold(self):
        self.assertEqual(main.create_threshold(0), (0, 0))


if __name__ == '__main__':
    unittest.main()
