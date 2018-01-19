# coding=utf-8
from operator import attrgetter

import operator

import sqlite3

from db_facade import DBFacade
from language.language_identifier import preprocess_text
from language.rhymer import Rhymer
from language.syllables import Syllabler

phrase = u"Buon appetito!"

phrase2 = preprocess_text(phrase)

rhyme_with = phrase2.split(' ')[-1]

dbf = DBFacade('data/phtitles.sqldb')

ls = Syllabler().syllables(rhyme_with).split('-')[-1]

titles = dbf.get_titles_by_last_syllable(ls, 'italian')

titles = [t for t in titles if t["LAST_WORD"] != rhyme_with and not t["LAST_WORD"] in rhyme_with
          and not rhyme_with in t["LAST_WORD"]]
#titles = [t for t in titles if t.last_word != rhyme_with]

def wnear (w1,w2):

    near = 0

    if len(w1) == 0 or len(w2) == 0:
        return 0

    for i in range(min([len(w1),len(w2)])):

        a = w1[len(w1)-i-1]
        b = w2[len(w2)-i-1]

        if a != b:
            break
        else:
            near += 1

    return near

titles = [(t,wnear(t["LAST_WORD"],rhyme_with)) for t in titles]

titles = sorted(titles, key=operator.itemgetter(1),reverse=True)


print phrase
print '\n'

for i in range(min([10, len(titles)])):

    print titles[i][0]["TITLE"] + ": " + titles[i][0]["LINK"]

rm = Rhymer(dbf,Syllabler())

print rm.rhyme(phrase)[0]

