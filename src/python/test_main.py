import unittest
import main


def setUpModule():
    """Disable logging while doing these tests."""
    logging.disable()


def tearDownModule():
    """Re-enable logging after doing these tests."""
    logging.disable(logging.NOTSET)


class TestMain(unittest.TestCase):

    def test_create_threshold(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
