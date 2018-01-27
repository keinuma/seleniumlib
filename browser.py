""""
2017/09/27 numata
This code get browser information, set url
"""

import os
import json
from selenium.webdriver.common.alert import Alert
from selenium.webdriver import Chrome, Ie, Safari, Edge, Firefox
from selenium.common.exceptions import WebDriverException, NoAlertPresentException
from selenium.webdriver.chrome.options import Options


class DriverProperty(object):
    """
    selenium webdriverのラッパー
    """

    def __init__(self, headless=False):
        """
        :param
        params['browser']: string: ブラウザ名
        base_url: string: URL
        headless: bool: ヘッドレスオプション
        """
        self.driver = None
        self.params = load_params()
        self.options = Options()
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--disable-web-security")
        if headless:
            self.options.add_argument("--headless")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--disable-desktop-notifications")
            self.options.add_argument("--disable-extensions")

    def set_driver(self, driver=None):
        """
        driverの引き継ぎに使用する
        :param driver: webdriver
        :return:
        """
        self.driver = driver
        return self

    def _open_browser(self):
        """
        :return webdriver:
        """
        if self.params['browser'] == 'chrome':
            self.driver = Chrome(chrome_options=self.options)
            self.driver = Chrome()
        elif self.params['browser'] == 'ie':
            self.driver = Ie()
        elif self.params['browser'] == 'safari':
            self.driver = Safari()
        elif self.params['browser'] == 'edge':
            self.driver = Edge()
        elif self.params['browser'] == 'firefox':
            self.driver = Firefox()
        else:
            raise Exception('Faild input browser name')
        self.driver.get(self.params['base_url'])
        return self.driver

    def visit(self, url):
        """
        :param url: string
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
        :return url: string
        """
        return self.driver.current_url

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
        :param user_name: string
        :param pass_word: string
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


def load_params():
    """
    :return: dict - driverクラスのインスタンス引数
    """
    list_dir = os.listdir('./')
    if 'config.json' in list_dir:
        with open('config.json') as f:
            params = json.load(f)
        return params
    else:
        return None
