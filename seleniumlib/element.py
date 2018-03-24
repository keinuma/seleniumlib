"""
2017/11/02 numata
This code is find element in html.
Save element and make actions.
"""

import time
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from .browser import DriverProperty


class ElementProperty(DriverProperty):
    """ input browser name and base url """

    def __init__(self, base_url=None, driver=None, headless=False):
        """
        ウェブドライバーを作成するか、引き継ぐ
        :param selenium.webdriver driver: ドライバー
        :param bool headless: ヘッドレスオプション
        """
        if driver is None:
            super().__init__(base_url=base_url, headless=headless)
        elif driver is not None:
            self.driver = driver
        else:
            raise ValueError('Value Error because url or webdriver is not found.')
        self._page_id = []
        self.elements = []

    def get_elements(self, tag='input', remove=False, init=0):
        """
        :param:tag: string select element tag(a, input, label)
        :param:remove: bool remove element saved
        :param:init: int skip element
        """
        try:
            self.elements = self.driver.find_elements_by_css_selector(tag)
        except NoSuchElementException:
            print('No such a selector {}'.format(tag))
            self.elements = []
        else:
            self.elements = self.elements[init:]
            self._delete_unvisual()
            # remove element saved in page id list
            if remove:
                self._delete_registered()
            self._update_page_id()

    def push_elements(self, elem=0, word=None):
        """
        elementsに対する操作を行う
        :param elem: int elementsリストのindex
        :param word: string 入力する文字列
        :return:
        """
        if not isinstance(elem, int):
            raise Exception('Input int index')
        if word is None:
            actions = ActionChains(self.driver)
            actions.move_to_element(self.elements[elem])
            actions.click(self.elements[elem])
            actions.perform()
            actions.reset_actions()
        elif isinstance(word, str):
            self.elements[elem].send_keys(word)
        else:
            raise Exception("Input string word(second arg)")

    def select(self, elem=0, index=0):
        """
        プルダウンリストの選択
        :param elem: int element listのindex
        :param index: int プルダウンのindex
        :return:
        """
        actions = ActionChains(self.driver)
        actions.move_to_element(self.elements[elem])
        actions.perform()
        actions.reset_actions()
        select = Select(self.elements[elem])
        select.select_by_index(index)

    def _delete_unvisual(self):
        """
        見えないelementを削除する
        :return:
        """
        if isinstance(self.elements, list) is False:
            raise Exception('Input value is not list')
        self.elements = [element
                         for element in self.elements
                         if element.is_displayed()]

    def _update_page_id(self):
        """
        page_idに現在のelement listを追加する
        :return:
        """
        self._page_id += [element.id for element in self.elements]

    def _delete_registered(self):
        """
        取得したelementからpage_idとの重複を削除する
        :return:
        """
        if isinstance(self.elements, list) is False:
            raise Exception('Input value is not list')
        self.elements = [element
                         for element in self.elements
                         if element.id not in self._page_id]

    def print(self):
        """
        elementの文字列を標準出力する
        :return:
        """
        out = 'index: {}, text: {}'
        for index, element in enumerate(self.elements):
            print(out.format(index, element.text))

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
            # scroll_width = 0
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
                        self.driver.execute_script("window.scrollBy(" + str(view_width) + ",0)")

                    tmpname = filepath + '/tmp_%d_%d.png' % (row_count, col_count)
                    self.driver.get_screenshot_as_file(tmpname)
                    time.sleep(3)

                    # 右端か下端に到達したら画像を切り取ってstitched_imageに貼り付ける
                    if scroll_width + view_width >= total_width or scroll_height + view_height >= total_height:
                        new_width = view_width
                        new_height = view_height
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
