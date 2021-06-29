import unittest
import main
import logging


def setUpModule():
    """Disable logging while doing these tests."""
    logging.disable()


def tearDownModule():
    """Re-enable logging after doing these tests."""
    logging.disable(logging.NOTSET)


class TestCreateThreshold(unittest.TestCase):
    """Tests for function ‘create_threshold’."""
    def test_create_threshold_zero(self):
        """Returns zeros for partial of 0 Hz."""
        self.assertEqual(main.create_threshold(0), (0, 0))


if __name__ == '__main__':
    unittest.main()
