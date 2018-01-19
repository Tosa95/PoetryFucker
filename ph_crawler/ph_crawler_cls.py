from Queue import Queue
import time

import requests
from bs4 import BeautifulSoup

from async_task import AsyncTask
from db_facade import Title
from language.language_identifier import preprocess_text


class PHCrawler (AsyncTask):

    def __init__(self, language_identifier, db_facade, syllabler, queue_max_size=3000, wait_btw_req = 3):

        super(PHCrawler, self).__init__()
        self._link_queue = Queue()
        self._li = language_identifier
        self._dbf = db_facade
        self._queue_max_size = queue_max_size
        self._wait_btw_req = wait_btw_req
        self._syllabler = syllabler

    def _worker(self, args):

        li = self._li

        dbf = self._dbf

        videos = []

        while not self._link_queue.empty() and not self._mustBeAborted:

            try:

                time.sleep(self._wait_btw_req)

                link = self._link_queue.get()

                page = requests.get(link)

                soup = BeautifulSoup(page.content, 'html.parser')

                for video in list(soup.find_all(class_="thumbnail-info-wrapper")):

                    tit = list(video.find_all(class_="title"))[0]

                    a = list(tit.find_all("a"))[0]

                    title = a['title']

                    maxlen = max([len(x) for x in title.split('-')])

                    title = [x for x in title.split('-') if len(x) == maxlen][0].strip()

                    lk = "https://it.pornhub.com" + a["href"]

                    views = list(list(video.find_all(class_="views"))[0].find_all("var"))[0].text

                    likes = list(video.find_all(class_="value"))[0].text

                    lang = li.identify_lang(title)

                    present = dbf.has_ph_title(title)

                    titlepr = preprocess_text(title)

                    words = titlepr.split(' ')

                    lw = words[-1]

                    ls = self._syllabler.syllables(lw).split('-')[-1]

                    title_data = {"TITLE": title,
                                  "LINK": lk,
                                  "VIEWS": views,
                                  "LIKES": likes,
                                  "LANGUAGE": lang,
                                  "LAST_WORD": lw,
                                  "LAST_SYLLABLE": ls}

                    try:
                        if not present:
                            videos.append(title_data)
                    except Exception as e:
                        print e

                    if self._link_queue.qsize() < self._queue_max_size and not present:
                        self._link_queue.put(lk)

                    print "%s ---> %s [%s %s]\t\t\tProbable language: %s" % (lk, title, views, likes, lang)

                self._dbf.add_titles(videos)
                videos = []

                print "QSIZE: %d" % self._link_queue.qsize()

            except Exception as ex:

                print ex

                


    def start(self,seed):

        self._link_queue.put(seed)
        self._startWorkerThread(name="PHCrawler", args=("aaa",))

