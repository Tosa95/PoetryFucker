# coding=utf-8
import json

import time

from db_facade import DBFacade
from language.language_identifier import FrequencyLanguageIdentifier, load_dictionary, DictionaryLanguageIdentifier
from language.syllables import Syllabler
from ph_crawler.ph_crawler_cls import PHCrawler

#data = {}

#with open("letter_lang_data","r") as f:

#    data = json.loads(f.read())

#data = {k:v for k,v in data.iteritems() if k == 'italian' or k == 'english'}

#li = FrequencyLanguageIdentifier(data)

dictionary = load_dictionary({"english":"data/english_words.json",
                              "italian":"data/italian_words.json"})

li = DictionaryLanguageIdentifier(dictionary)

dbf = DBFacade("data/phtitles.sqldb")

phc = PHCrawler(li, dbf, Syllabler())

phc.start("https://it.pornhub.com")

try:
    while True:
        time.sleep(1)
except Exception:
    phc.abort()