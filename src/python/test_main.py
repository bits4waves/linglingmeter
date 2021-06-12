import unittest
import main


def setUpModule():
    """Disable logging while doing these tests."""
    logging.disable()


def tearDownModule():
    """Re-enable logging after doing these tests."""
    logging.disable(logging.NOTSET)


class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        self.fail()


    @classmethod
    def tearDownClass(cls):
        self.fail()


    def setUp(self):
        self.fail()


    def tearDown(self):
        self.fail()


    def test_something(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
