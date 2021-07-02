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


    def test_create_threshold_octave(self):
        """Returns octaves for threshold of 1200 cents."""
        self.assertEqual(main.create_threshold(440, 1200),
                         (220.0, 880.0))


    def test_create_threshold_default_cents(self):
        """Uses 50 cents as default value for threshold."""
        f0, cents = 440, 50
        self.assertAlmostEqual(
            main.create_threshold(f0),
            (f0 * pow(2, -cents/1200), f0 * pow(2, cents/1200)))


class TestGetThreshold(unittest.TestCase):
    """Tests for function ‘get_threshold’."""
    def test_get_threshold_from_empty(self):
        """Gets the first threshold from an empty list."""
        thresholds = []
        # Using a value for cents different from the default on
        # purpose.
        f0, cents = 440, 51
        self.assertAlmostEqual(
            main.get_threshold(thresholds, 0, f0, cents=cents),
            (f0 * pow(2, -cents/1200), f0 * pow(2, cents/1200)))


    def test_get_threshold_from_not_empty(self):
        """Gets the thresholds from a non-empty list."""
        # Using a value for cents different from the default on
        # purpose.
        f0, cents = 440, 51
        thresholds = [(f0 * pow(2, -cents/1200),
                       f0 * pow(2, cents/1200))]
        partial = {}
        partial['n'] = 2
        partial['f'] = partial['n'] * f0
        self.assertAlmostEqual(
            main.get_threshold(thresholds, 1, f0, cents=cents),
            (f0 * pow(2, -cents/1200), f0 * pow(2, cents/1200)))


if __name__ == '__main__':
    unittest.main()
