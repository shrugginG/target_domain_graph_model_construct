import unittest
import datetime


class MyTestCase(unittest.TestCase):
    def test_something(self):
        print(str(datetime.datetime.now()).split('.')[0])


if __name__ == '__main__':
    unittest.main()
