'''
2017/11/02 numata
This code is find element in html.
Save element and make actions.
'''

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from browser import DriverProperty


class ElementProperty(DriverProperty):
    """ input browser name and base url """

    def __init__(self, browser='chrome', baseurl=None, driver=None):
        """ input URL
        :type baseurl: str
        :type driver: selenium.webdriver
        """
        if baseurl != None:
            super().__init__(browser, baseurl)
            super().open_browser()
        elif driver != None:
            self.driver = driver
        else:
            raise ValueError("Input baseurl or driver")
        self.page_id = []
        self.elements = []

    def get_elements(self, tag='input', remove=0, init=0):
        """
        arg detail
        tag: select element tag (a, input, label)
        remove: remove element saved
        init: skip element
        """
        try:
            self.elements = self.driver.find_elements_by_css_selector(tag)
        except NoSuchElementException:
            print('No such a selector {}'.format(tag))
            self.elements = []
        else:
            self.elements = self.elements[init:]
            self.delete_unvisual()
            # remove element saved in page id list
            if remove == 1:
                self.delete_registered()
            self.update_page_id()

    def push_elements(self, elem=0, word=None):
        """ check send word is str """
        if not isinstance(elem, int):
            raise Exception('Plese input int index')
        if word is None:
            self.elements[elem].click()
        elif isinstance(word, str):
            self.elements[elem].send_keys(word)
        else:
            raise Exception("Plese input string word(second arg)")

    def select(self, elem=0, index=0):
        """ operation select element """
        select = Select(self.elements[elem])
        select.select_by_index(index)

    def delete_unvisual(self):
        """ extract visuable element in html """
        if isinstance(self.elements, list) is False:
            raise Exception('Input value is not list')
        self.elements = [element
                         for element in self.elements
                         if element.is_displayed()]

    def update_page_id(self):
        """ add input elements page id """
        self.page_id += [element.id for element in self.elements]

    def delete_registered(self):
        """ extract elements not include element id """
        if isinstance(self.elements, list) is False:
            raise Exception('Input value is not list')
        self.elements = [element
                         for element in self.elements
                         if element.id not in self.page_id]

    def print(self):
        """ check html text is correct"""
        for index, element in enumerate(self.elements):
            print(index, element.text)
