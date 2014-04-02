import unittest

class TestSome(unittest.TestCase):
    def test_simple(self):
        x = 1
        y = 2
        self.assertEquals(x, y)

    def test_simple2(self):
        x = 1
        y = 1
        self.assertEquals(x, y)

    def test_simple3(self):
        x = 1
        y = 1 / 0

if __name__ == "__main__":
    unittest.main()
