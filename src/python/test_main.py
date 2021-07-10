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


class TestIntegratePeaks(unittest.TestCase):
    """Tests for function ‘integrate_peaks’."""
    def test_silence(self):
        """Returns 0 for an empty spectrum."""
        self.assertEqual(
            main.integrate_peaks(f0=0, frequencies=[], spectrum=[]),
            0)


    def test_sole_peak(self):
        """Returns the sole peak's value for an individual peak."""
        f0 = 440
        frequencies = [440]
        spectrum = [1.0]
        self.assertEqual(
            main.integrate_peaks(f0, frequencies, spectrum),
            1.0)


    def test_sole_peak_with_tail(self):
        """Returns sum of the peak's value plus its tails' values."""
        f0 = 440
        frequencies = [430, 435, 440, 445, 450]
        spectrum = [0.0, 1.0, 2.0, 4.0, 0.0]
        self.assertEqual(
            main.integrate_peaks(f0, frequencies, spectrum),
            7.0)


    def test_two_peaks(self):
        """Returns the two individual peaks' value."""
        f0 = 440
        frequencies = [440, 880]
        spectrum = [1.0, 2.0]
        self.assertEqual(
            main.integrate_peaks(f0, frequencies, spectrum),
            3.0)


    def test_two_peaks_with_tails(self):
        """Returns the two peaks' value plus their tails'."""
        f0 = 440
        frequencies = [220,
                       439, 440, 441,
                       880,
                       1759, 1760, 1761,
                       3520]
        spectrum = [0.0,
                    1.0, 2.0, 4.0,
                    0.0,
                    8.0, 16.0, 32.0,
                    0.0]
        self.assertEqual(
            main.integrate_peaks(f0, frequencies, spectrum),
            63.0)


if __name__ == '__main__':
    unittest.main()
