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
    def setUp(self):
        self.f0 = 440
        self.cents = 51


    def test_get_threshold_from_empty(self):
        """Gets the first threshold from an empty list."""
        thresholds = []
        self.assertAlmostEqual(
            main.get_threshold(thresholds, 0, self.f0,
                               cents=self.cents),
            (self.f0 * pow(2, -self.cents/1200),
             self.f0 * pow(2, self.cents/1200)))


    def test_get_threshold_from_not_empty(self):
        """Gets the thresholds from a non-empty list."""
        thresholds = []
        thresholds.append((self.f0 * pow(2, -self.cents/1200),
                           self.f0 * pow(2, self.cents/1200)))

        partial = {}
        partial['n'] = 2
        partial['f'] = partial['n'] * self.f0
        self.assertAlmostEqual(
            main.get_threshold(thresholds, 1, self.f0,
                               cents=self.cents),
            (partial['f'] * pow(2, -self.cents/1200),
             partial['f'] * pow(2, self.cents/1200)))


    def test_get_threshold_skipping(self):
        """Gets the thresholds, skipping a partial."""
        thresholds = []
        # Append the fundamental.
        thresholds.append((self.f0 * pow(2, -self.cents/1200),
                           self.f0 * pow(2, self.cents/1200)))
        # Append the first upper partial.
        partial = {}
        partial['n'] = 2
        partial['f'] = partial['n'] * self.f0
        threshold = (partial['f'] * pow(2, -self.cents/1200),
                     partial['f'] * pow(2, self.cents/1200))
        thresholds.append(threshold)

        self.assertAlmostEqual(
            main.get_threshold(thresholds, 1, self.f0,
                               cents=self.cents),
            threshold)


class TestIntegratePeaks(unittest.TestCase):
    """Tests for function ‘integrate_peaks’."""
    def test_silence(self):
        """Returns 0 for an empty spectrum."""
        self.assertEqual(
            main.integrate_peaks(f0=0, thresholds=[], frequencies=[],
                                 spectrum=[]),
            0)


    def test_sole_peak(self):
        """Returns the sole peak's value for an individual peak."""
        f0 = 440
        thresholds = []
        frequencies = [440]
        spectrum = [1.0]
        self.assertEqual(
            main.integrate_peaks(f0, thresholds, frequencies,
                                 spectrum),
            1.0)


    def test_sole_peak_with_tail(self):
        """Returns sum of the peak's value plus its tails' values."""
        f0 = 440
        thresholds = [(435, 445)]
        frequencies = [430, 435, 440, 445, 450]
        spectrum = [0.0, 1.0, 2.0, 4.0, 0.0]
        self.assertEqual(
            main.integrate_peaks(f0, thresholds, frequencies,
                                 spectrum),
            7.0)


if __name__ == '__main__':
    unittest.main()
