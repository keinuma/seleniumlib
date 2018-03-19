""""
2017/09/27 numata
This code get browser information, set url
"""

from selenium.webdriver.common.alert import Alert
from selenium.webdriver import Chrome, Ie, Safari, Edge, Firefox
from selenium.common.exceptions import WebDriverException, NoAlertPresentException
from selenium.webdriver.chrome.options import Options


class DriverProperty(object):
    """
    selenium webdriverのラッパー
    """

    def __init__(self, base_url=None, headless=False, browser_name='chrome'):
        """
        :param bool headless: ヘッドレスオプション
        :return:
        """
        self.driver = None
        self.base_url = base_url
        self.options = Options()
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--disable-web-security")
        if headless:
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--disable-desktop-notifications")
            self.options.add_argument("--disable-extensions")
        self._open_browser(browser_name=browser_name.lower())

    def set_driver(self, driver=None):
        """
        driverの引き継ぎに使用する
        :param selenium.webdriver driver: 引き継ぎ対象
        :return: DriverProperty self
        """
        self.driver = driver
        return self

    def _open_browser(self, browser_name):
        """
        :return: webdriver
        """
        if browser_name == 'chrome':
            if self.options is not None:
                self.driver = Chrome(chrome_options=self.options)
            else:
                self.driver = Chrome()
        elif browser_name == 'ie':
            self.driver = Ie()
        elif browser_name == 'safari':
            self.driver = Safari()
        elif browser_name == 'edge':
            self.driver = Edge()
        elif browser_name == 'firefox':
            self.driver = Firefox()
        else:
            raise Exception('Faild input browser name')
        self.driver.get(self.base_url)
        return self.driver

    def visit(self, url):
        """
        :param str url:
        :return: self
        """
        if url is None:
            raise Exception('input url.')
        try:
            self.driver.get(url)
        except WebDriverException:
            print('No such a url')
            self.driver.quit()

    def current_url(self):
        """
        :return: string
        """
        return self.driver.current_url()

    def close(self):
        """
        driverはクローズしない
        :return:
        """
        self.driver.close()

    def refresh(self):
        """
        現在のURLを開き直す
        :return:
        """
        self.driver.refresh()

    def authentication(self, user_name, pass_word):
        """
        ログイン認証を行う
        :param str user_name: ユーザ名
        :param str pass_word: パスワード
        :return:
        """
        self.driver.switch_to.alert.authenticate(user_name, pass_word)

    def accept(self):
        """
        警告を承認
        :return:
        """
        try:
            Alert(self.driver).accept()
        except NoAlertPresentException:
            pass

