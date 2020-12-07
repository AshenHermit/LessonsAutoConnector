from splinter import Browser
import time

import splinter
from selenium import webdriver

import re
import datetime
import time

class Connector:
    def __init__(self, username):
        self.username = username

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("user-data-dir=C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data")
        self.browser = Browser('chrome', options=self.chrome_options)

        self.browser.visit("https://dnevnik.mos.ru/diary/diary/lessons")

        self.lessons = []
        self.lessonEls = None

    def gather_lessons(self):
        global lessons, lessonEls

        lessonEls = None
        while not lessonEls:
            lessonEls = self.browser.find_by_css('*[class="css-1dbjc4n r-14lw9ot r-5qlx7g r-nefvgx r-1vznrp2 r-3f7b68 r-eqz5dr r-d23pfw"]')

        lessonEls = lessonEls[0].find_by_css('*[class="css-1dbjc4n r-eqz5dr r-1wbh5a2 r-1777fci r-5oul0u"]')
        lessons = []
        for l in lessonEls:
            result = re.match(r'\d\n(.*?):(.*?) — (.*?):(.*?)\n', l.text)
            if result:
                lessons.append({'el':l, 'start_time': [int(result[1]), int(result[2])], 'end_time':[int(result[3]), int(result[4])]})

        print(lessonEls)

    def wait_click(self, query):
        button = None
        while not button:
            button = self.browser.find_by_css(query)
        button[0].click()

    def wait_input(self, query, text):
        input = None
        while not input:
            input = self.browser.find_by_css(query)
        input[0].value = text


    def connect_to_next_lesson(self):
        finded = None
        # finded = lessons[5]
        while not finded:
            t = datetime.datetime.now().time()
            for l in lessons:
                if t.hour >= l['start_time'][0] and t.minute >= l['start_time'][1]\
                and (t.hour < l['end_time'][0] or (t.hour == l['end_time'][0] and t.minute <= l['end_time'][1]-16)):
                    finded = l

            time.sleep(0.5)
                    
        finded['el'].click()

        self.wait_click('*[class="css-1dbjc4n r-1loqt21 r-p1pxzi r-dnmrzs r-1otgn73 r-eafdt9 r-1i6wzkk r-lrvibr r-fsuzt3"')

        self.browser.windows.current = self.browser.windows[1]

        self.wait_click('*[data-tid="joinOnWeb"')

        self.wait_input('#username', self.username)

        self.wait_click('*[data-tid="prejoin-join-button"')

        ended = False
        while not ended:
            t = datetime.datetime.now().time()
            if (t.hour > finded['end_time'][0]) or (t.hour == finded['end_time'][0] and t.minute >= finded['end_time'][1]-15):
                guys = self.browser.find_by_css('*[class="item vs-repeat-repeated-element"')
                if guys:
                    if len(guys) <= 3:
                        ended = True

            time.sleep(0.5)

        self.wait_click('*[data-tid="call-hangup"]')
        self.browser.windows[1].close
        self.browser.windows.current = self.browser.windows[0]

    def start(self):
        while True:
            self.gather_lessons()
            self.connect_to_next_lesson()