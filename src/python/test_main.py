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
        self.assertAlmostEqual(main.create_threshold(440),
                               (427.4740541075866,
                                452.8929841231365))


class TestGetThreshold(unittest.TestCase):
    """Tests for function ‘get_threshold’."""
    def test_get_threshold_from_empty(self):
        """Gets the first threshold from an empty list."""
        thresholds = []
        i = 0
        f0 = 440
        self.assertAlmostEqual(
            main.get_threshold(thresholds, 0, 440),
            (427.4740541075866, 452.8929841231365))


if __name__ == '__main__':
    unittest.main()
