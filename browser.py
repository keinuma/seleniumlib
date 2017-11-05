""""
2017/09/27 numata
This code get browser information, set url
"""

from selenium.webdriver.common.alert import Alert
from selenium.webdriver import Chrome, Ie, Safari, Edge, Firefox
from selenium.common.exceptions import WebDriverException, NoAlertPresentException
from seleniumlib.config import BROWSER_NAME, BASE_URL


class DriverProperty(object):
    ''' making base driver for selenium.'''

    def __init__(self, browser_name=BROWSER_NAME, base_url=BASE_URL):
        ''' useful browser is chrome, ie, safari, edge, firefox '''
        self.browser_name = browser_name
        self.driver = None
        self.base_url = base_url

    def set_driver(self, browser_name=BROWSER_NAME, base_url=BASE_URL):
        ''' if driver have value, driver close browser '''
        self.browser_name = browser_name
        self.base_url = base_url
        self.open_browser()

    def open_browser(self):
        ''' before extract this function, plese set self.browser_name '''
        if self.browser_name == 'chrome':
            self.driver = Chrome()
        elif self.browser_name == 'ie':
            self.driver = Ie()
        elif self.browser_name == 'safari':
            self.driver = Safari()
        elif self.browser_name == 'edge':
            self.driver = Edge()
        elif self.browser_name == 'firefox':
            self.driver = Firefox()
        else:
            raise Exception('Faild input browser name')
        self.driver.get(self.base_url)

    def visit(self, url=None):
        ''' open args url or setted base url. '''
        if url is None and self.base_url is None:
            raise Exception('Plese input url.')
        self.base_url = url
        try:
            self.driver.get(self.base_url)
        except WebDriverException:
            print('No such a url')
        finally:
            self.driver.quit()

    def current_url(self):
        ''' get current url '''
        return self.driver.current_url

    def close(self):
        ''' close tab, not stop driver '''
        self.driver.close()

    def refresh(self):
        ''' reopen current url '''
        self.driver.refresh()

    def authentication(self, user_name, pass_word):
        ''' accept authenticate '''
        self.driver.switch_to.alert.authenticate(user_name, pass_word)

    def accept(self):
        ''' accept page aleart, example(This page is not safe) '''
        try:
            Alert(self.driver).accept()
        except NoAlertPresentException:
            pass
