# coding=utf-8
from operator import attrgetter

import operator

from db_facade import DBFacade
from language.language_identifier import preprocess_text
from language.syllables import Syllabler

phrase = u"In bocca al lupo!"

phrase2 = preprocess_text(phrase)

rhyme_with = phrase2.split(' ')[-1]

dbf = DBFacade('data/phtitles.sqldb')

ls = Syllabler().syllables(rhyme_with).split('-')[-1]

titles = dbf.get_titles_by_last_syllable(ls, 'italian')

titles = [t for t in titles if t.last_word != rhyme_with and not t.last_word in rhyme_with and not rhyme_with in t.last_word]
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

titles = [(t,wnear(t.last_word,rhyme_with)) for t in titles]

titles = sorted(titles, key=operator.itemgetter(1),reverse=True)


print phrase
print '\n'

for i in range(min([10,len(titles)])):

    print titles[i][0].title + ": " + titles[i][0].link
