import os

import requests
import time
from bs4 import BeautifulSoup
#http://www.divisioneinsillabe.it/dividi/asta

#Main directory of the application
from db_facade import DBFacade

MAIN_DIRECTORY = os.path.dirname(__file__)

#Directory in which to store data
DATA_DIRECTORY = os.path.join(MAIN_DIRECTORY, "data")

DICTIONARY_FILE = os.path.join(DATA_DIRECTORY, "lista_badwords.txt")

SYLLABLED_DICTIONARY_FILE = os.path.join(DATA_DIRECTORY, "db.sqldb")

dbfc = DBFacade(SYLLABLED_DICTIONARY_FILE)

with open(DICTIONARY_FILE, 'r') as f:

    words = f.readlines()

total = len(words)
i = 1

for word in words:

    word = word.strip('\r\n')

    try:

        perc = (float(i) / float(total)) * 100.0

        if not dbfc.has_word(word):

            page = requests.get("http://www.divisioneinsillabe.it/dividi/%s" % word)

            soup = BeautifulSoup(page.content, 'html.parser')

            syllables = soup.find_all(id="res")[0].get_text().strip('\r\n')

            dbfc.add_word(word, syllables)

            print "[%3.4f%%]: %s --> %s" % (perc, word, syllables)

            time.sleep(0.1)

        else:

            print "[%3.4f%%]: %s --> skipped because already present in db" % (perc, word)

    except Exception as ex:

        print ex

    finally:

        i += 1


