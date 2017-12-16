'''
2017/11/02 numata
This code is find element in html.
Save element and make actions.
'''

import time
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from seleniumlib.browser import DriverProperty


class ElementProperty(DriverProperty):
    """ input browser name and base url """

    def __init__(self, browser='chrome', baseurl=None, driver=None,
                 headless=False):
        """ input URL
        :type baseurl: str
        :type driver: selenium.webdriver
        """
        if baseurl is not None:
            super().__init__(browser, baseurl, headless)
            super().open_browser()
        elif driver is not None:
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
            ActionChains(
                self.driver
            ).move_to_element(
                self.elements[elem]
            ).click(
                self.elements[elem]
            ).perform()
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

    def save_screenshot(self, filename, fullsize=False):
        filepath = '/'.join(filename.split('/')[:-1])
        if fullsize:
            # ページの左上までスクロール
            self.driver.execute_script("window.scrollTo(0, 0);")

            # ページサイズ取得
            total_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            total_width = self.driver.execute_script(
                "return document.body.scrollWidth"
            )

            # 画面サイズ取得
            view_width = self.driver.execute_script(
                "return window.innerWidth"
            )
            view_height = self.driver.execute_script(
                "return window.innerHeight"
            )

            # 画像処理用
            stitched_image = Image.new("RGB", (total_width, total_height))

            # スクロール操作用
            scroll_width = 0
            scroll_height = 0

            row_count = 0
            # 縦スクロールの処理§
            while scroll_height < total_height:
                # 横スクロール初期化
                col_count = 0
                scroll_width = 0
                self.driver.execute_script("window.scrollTo(%d, %d)" % (scroll_width, scroll_height)) 
                # 横スクロールの処理
                while scroll_width < total_width:
                    if col_count > 0:
                        # 画面サイズ分横スクロール
                        self.driver.execute_script("window.scrollBy("+str(view_width)+",0)") 

                    tmpname = filepath + '/tmp_%d_%d.png' % (row_count, col_count)
                    self.driver.get_screenshot_as_file(tmpname)
                    time.sleep(3)

                    # 右端か下端に到達したら画像を切り取ってstitched_imageに貼り付ける
                    if scroll_width + view_width >= total_width or scroll_height + view_height >= total_height:
                        new_width = view_width
                        new_height= view_height
                        if scroll_width + view_width >= total_width:
                            new_width = total_width - scroll_width
                        if scroll_height + view_height >= total_height:
                            new_height = total_height - scroll_height
                        tmp_image = Image.open(tmpname)
                        tmp_image.crop(
                            (view_width - new_width, view_height - new_height, view_width, view_height)
                        ).save(tmpname)
                        stitched_image.paste(
                            Image.open(tmpname),
                            (scroll_width, scroll_height))
                        scroll_width += new_width

                    # 普通に貼り付ける
                    else:
                        stitched_image.paste(
                            Image.open(tmpname),
                            (scroll_width, scroll_height))
                        scroll_width += view_width
                        col_count += 1

                scroll_height += view_height
                time.sleep(3)

            # 指定のfilenameにstitched_image格納
            stitched_image.save(filename)
            return True

        # fullsize=Falseの場合は通常のスクリーンショットを取得
        else:
            self.driver.get_screenshot_as_file(filename)
