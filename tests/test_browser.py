import time
import unittest
from seleniumlib import browser

class TestDriverProperty(unittest.TestCase):
    """
    browser.pyの各メソッドのテスト
    """

    def setUp(self):
        """
        :return:
        """
        self.url = 'https://google.com'
        self.browser = browser.DriverProperty()

    def test_visit(self):
        """
        visitメソッドテスト
        :return:
        """
        self.browser.visit(self.url)
        self.assertEqual(
            self.url,
            self.browser.driver.current_url
        )

