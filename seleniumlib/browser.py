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
        :param bool headless: ヘッドレスオプション
        :return:
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
        self._open_browser()

    def set_driver(self, driver=None):
        """
        driverの引き継ぎに使用する
        :param selenium.webdriver driver: 引き継ぎ対象
        :return: DriverProperty self
        """
        self.driver = driver
        return self

    def _open_browser(self):
        """
        :return: webdriver
        """
        if self.params['browser'] == 'chrome':
            if self.options is not None:
                self.driver = Chrome(chrome_options=self.options)
            else:
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


def load_params():
    """
    :return: dict - driverクラスのインスタンス引数
    """
    config_dir = input('Please input json file directory: ')
    list_dir = os.listdir(config_dir)
    if 'config.json' in list_dir:
        path = os.path.join(config_dir, 'config.json')
        with open(path) as f:
            params = json.load(f)
        return params
    else:
        return None
