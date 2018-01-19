import sqlite3

import time
from collections import namedtuple
from sqlite3 import IntegrityError

Title = namedtuple("Title", "link title views likes language last_syllable last_word")

class DBFacade:

    def _getConn(self):

        conn = sqlite3.connect(self._dbaddr)
        conn.row_factory = sqlite3.Row
        return conn

    def _exec(self, cursor, query, parameters):

        cursor.execute(query, parameters)
        return cursor.fetchall()

    def _exec_multiple(self, query, parameters_list):

        conn = self._getConn()

        cursor = conn.cursor()
        res = []

        for param in parameters_list:

            try:
                r = self._exec(cursor, query, param)
                res.append(r)
            except Exception as ex:
                res.append(ex)

        conn.commit()
        conn.close()

        return res

    def _exec_single(self, query, parameters):

        conn = self._getConn()

        cursor = conn.cursor()

        res = self._exec(cursor, query, parameters)

        conn.commit()
        conn.close()

        return res

    def __init__(self, dbaddr):

        self._dbaddr = dbaddr

        self._init_tables()

    def _init_tables(self):

        conn = self._getConn()

        conn.execute("""CREATE TABLE IF NOT EXISTS SYLLABLED_WORDS
                                    (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        WORD TEXT NOT NULL,
                                        SYLLABLES TEXT NOT NULL
                                    );
                                   """)

        conn.execute("""CREATE TABLE IF NOT EXISTS PH_TITLES
                                            (
                                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                LINK TEXT NOT NULL,
                                                TITLE TEXT NOT NULL UNIQUE,
                                                LAST_WORD TEXT,
                                                LAST_SYLLABLE TEXT,
                                                VIEWS TEXT,
                                                LIKES TEXT,
                                                LANGUAGE TEXT,
                                                DATE_ADDED TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                            );
                                           """)

        conn.commit()

        conn.close()

    def add_word(self,word,syllables):

        conn = sqlite3.connect(self._dbaddr)

        query = """INSERT INTO SYLLABLED_WORDS (WORD, SYLLABLES)
                              VALUES (\'%s\', \'%s\');""" % (word, syllables)

        cursor = conn.cursor()

        cursor.execute(query.encode('utf-8'))

        id = cursor.lastrowid

        conn.commit()

        conn.close()

        return id

    def has_word(self, word):

        conn = sqlite3.connect(self._dbaddr)

        query = """SELECT WORD FROM SYLLABLED_WORDS WHERE WORD='%s'""" % word

        #query = """SELECT WORD FROM SYLLABLED_WORDS"""

        cursor = conn.cursor()

        cursor.execute(query.encode('utf-8'))

        rows = cursor.fetchall()

        sz = len(rows)

        conn.close()

        return sz > 0

    def get_random_words(self,number):

        conn = sqlite3.connect(self._dbaddr)

        query = r"""SELECT WORD, SYLLABLES FROM SYLLABLED_WORDS ORDER BY random() LIMIT %d""" % number

        # query = """SELECT WORD FROM SYLLABLED_WORDS"""

        cursor = conn.cursor()

        cursor.execute(query.encode('utf-8'))

        rows = cursor.fetchall()

        conn.close()

        return rows

    def has_ph_title(self,title):
        conn = sqlite3.connect(self._dbaddr)

        query = r"""SELECT TITLE FROM PH_TITLES WHERE TITLE=?"""

        # query = """SELECT WORD FROM SYLLABLED_WORDS"""

        cursor = conn.cursor()

        cursor.execute(query,(title,))

        rows = cursor.fetchall()

        sz = len(rows)

        conn.close()

        return sz > 0

    def add_title(self,title,link,views,likes,language):


        query = """INSERT INTO PH_TITLES (TITLE,LINK,VIEWS,LIKES,LANGUAGE)
                                      VALUES (?, ?, ?, ?, ?);"""

        self._exec_single(query, (title, link, views, likes, language))


    def add_titles(self,titles):

        titles_param = [(x.get("TITLE"), x.get("LINK"), x.get("VIEWS"), x.get("LIKES"), x.get("LANGUAGE"),
                         x.get("LAST_WORD"), x.get("LAST_SYLLABLE")) for x in titles]

        query = """INSERT INTO PH_TITLES (TITLE,LINK,VIEWS,LIKES,LANGUAGE, LAST_WORD, LAST_SYLLABLE)
                                              VALUES (?,?,?,?,?,?,?);"""

        self._exec_multiple(query, titles_param)




    def add_titles_full(self,titles):

        conn = sqlite3.connect(self._dbaddr)

        try:
            cursor = conn.cursor()

            for title_data in titles:

                title = title_data.title

                try:
                    cursor.execute(r"""INSERT INTO PH_TITLES (TITLE,LINK,VIEWS,LIKES,LANGUAGE,LAST_WORD,LAST_SYLLABLE)
                                                          VALUES (?,?,?,?,?,?,?);""", (
                    title, title_data.link, title_data.views, title_data.likes, title_data.language,
                    title_data.last_word, title_data.last_syllable))

                except IntegrityError:

                    pass

            conn.commit()

        except Exception as ex:

            print ex

        finally:

            conn.close()

    def  count_titles(self):

        conn = sqlite3.connect(self._dbaddr)

        query = """SELECT TITLE FROM PH_TITLES"""

        # query = """SELECT WORD FROM SYLLABLED_WORDS"""

        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        sz = len(rows)

        conn.close()

        return sz

    def get_title_by_id(self,id):

        query = r"""SELECT * FROM PH_TITLES WHERE ID=?"""

        res = self._exec_single(query, (id,))

        if len(res) > 0:
            return res[0]
        else:
            return None

    def get_titles_by_last_syllable(self,syllable,lang):

        conn = sqlite3.connect(self._dbaddr)

        query = r"""SELECT LINK,TITLE,LAST_WORD,LAST_SYLLABLE,VIEWS,LIKES,LANGUAGE FROM PH_TITLES WHERE LAST_SYLLABLE=? AND LANGUAGE=?"""

        # query = """SELECT WORD FROM SYLLABLED_WORDS"""

        cursor = conn.cursor()

        cursor.execute(query,(syllable,lang))

        rows = cursor.fetchall()

        rows = [Title(link=link,title=title,last_word=last_word,last_syllable=last_syllable,views=views,likes=likes,language=language) for
                (link,title,last_word,last_syllable,views,likes,language) in rows]

        return rows

