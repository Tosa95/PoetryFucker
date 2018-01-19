#coding=utf-8

from db_facade import DBFacade, Title
from language.language_identifier import load_dictionary, DictionaryLanguageIdentifier, preprocess_text
from language.syllables import Syllabler

DBFILE1 = "data/prova.sqldb"
DBFILE2 = "data/corrected_lang.sqldb"

dbf1 = DBFacade(DBFILE1)
dbf2 = DBFacade(DBFILE2)

dictionary = load_dictionary({"english":"data/english_words.json",
                                      "italian":"data/italian_words.json"})

li = DictionaryLanguageIdentifier(dictionary)

sy = Syllabler()

titles = []

word = "ol' classic vintage ticklin'".replace("'","''")

for i in range(1,dbf1.count_titles()+1):
#for i in range(1,100):

    data = dbf1.get_title_by_id(i)

    #print data

    title = preprocess_text(data[2])

    words = title.split(' ')

    lw = words[-1]

    ls = sy.syllables(lw).split('-')[-1]

    title_data = Title(title=data[2],link=data[1],views=data[5],likes=data[6],
                       language=li.identify_lang(data[2]),last_word=lw,last_syllable=ls)

    titles.append(title_data)

    if i%300 == 0:
        print i
        dbf2.add_titles_full(titles)
        titles = []

dbf2.add_titles(titles)
