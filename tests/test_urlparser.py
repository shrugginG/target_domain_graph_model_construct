import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        from urllib.parse import urlparse

        url = """https://www.jiazhao.com/jiaojingshoushi/169/"""
        parse_result = urlparse(url)
        print(parse_result)


if __name__ == '__main__':
    unittest.main()
