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
                lessons.append({'el':l, 
                    'start_time': [int(result[1])*60 + int(result[2]), int(result[1]), int(result[2])], 
                    'end_time':   [int(result[3])*60 + int(result[4]), int(result[3]), int(result[4])]})

        print(lessonEls)

    def wait_click(self, query, id=0):
        button = None
        while not button:
            button = self.browser.find_by_css(query)
        button[id].click()

    def wait_input(self, query, text, id=0):
        input = None
        while not input:
            input = self.browser.find_by_css(query)
        input[id].value = text

    def get_current_time(self):
        t = datetime.datetime.now().time()
        t = t.hour * 60 + t.minute
        return t


    def connect_to_next_lesson(self):
        finded = None

        ## set custom lesson
        # finded = lessons[0]
   
        while not finded:
            t = self.get_current_time()
            for l in lessons:
                if t >= l['start_time'][0]\
                and t <= l['end_time'][0]-16:
                    finded = l

            time.sleep(2)
                    
        finded['el'].click()

        self.wait_click('.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary')

        self.browser.windows.current = self.browser.windows[1]
        self.browser.windows[0].close()

        # "продолжить в этом браузере"
        self.wait_click('*[data-tid="joinOnWeb"]')

        # "продолжить без звука и видео"
        self.wait_click('*[class="ts-btn ts-btn-fluent ts-btn-fluent-secondary-alternate"]')

        # username input
        self.wait_input('#username', self.username)

        # join bradcast
        self.wait_click('*[data-tid="prejoin-join-button"]')

        ended = False
        while not ended:
            t = self.get_current_time()
            if t >= finded['end_time'][0]-15:
                guys = self.browser.find_by_css('*[class="item vs-repeat-repeated-element"]')
                if guys:
                    if len(guys) <= 4:
                        ended = True

            if t >= finded['end_time'][0]:
                ended = True

            time.sleep(0.5)

        #self.wait_click('*[data-tid="call-hangup"]')

    def start(self):
        diary = "https://dnevnik.mos.ru/diary/diary/lessons"
        self.browser.visit(diary)
        
        while True:
            self.gather_lessons()
            self.connect_to_next_lesson()
            self.browser.visit(diary)