import json

import requests
from bs4 import BeautifulSoup

from db_facade import DBFacade
from language.language_identifier import FrequencyLanguageIdentifier

link = "https://it.pornhub.com/playlist/769991 "

page = requests.get(link)

soup = BeautifulSoup(page.content, 'html.parser')

data = {}

with open("letter_lang_data","r") as f:

    data = json.loads(f.read())

data = {k:v for k,v in data.iteritems() if k == 'italian' or k == 'english'}

li = FrequencyLanguageIdentifier(data)

dbf = DBFacade("prova.sqldb")

for video in list(soup.find_all(class_="thumbnail-info-wrapper")):

    tit = list(video.find_all(class_="title"))[0]

    a = list(tit.find_all("a"))[0]

    title = a['title']

    maxlen = max([len(x) for x in title.split('-')])

    title = [x for x in title.split('-') if len(x) == maxlen][0].strip()

    title = title.replace("'","''")

    lk = "https://it.pornhub.com" + a["href"]

    views = list(list(video.find_all(class_="views"))[0].find_all("var"))[0].text

    likes = list(video.find_all(class_="value"))[0].text

    lang = li.identify_lang(title)

    try:
        if not dbf.has_ph_title(title):
            dbf.add_title(title,lk,views,likes,lang)
    except Exception as e:
        print e

    if lang == 'italian':
        print "%s ---> %s [%s %s]\t\t\tProbable language: %s" % (lk,title,views,likes,lang)
