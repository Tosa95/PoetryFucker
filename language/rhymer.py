import operator

from helpers.sqlite_helpers import sqlite_row_to_dict


class Rhymer:

    def __init__(self,dbf,syllabler):

        self._dbf = dbf
        self._syllabler = syllabler

    def rhyme(self, phrase):

        phrase2 = self._syllabler.preprocess_text(phrase)

        rhyme_with = phrase2.split(' ')[-1]

        dbf = self._dbf

        ls = self._syllabler.syllables(rhyme_with).split('-')[-1]

        titles = dbf.get_titles_by_last_syllable(ls, 'italian')

        titles = [sqlite_row_to_dict(t) for t in titles]

        titles = [t for t in titles if t["LAST_WORD"] != rhyme_with and not t["LAST_WORD"] in rhyme_with
                  and not rhyme_with in t["LAST_WORD"]]

        # titles = [t for t in titles if t.last_word != rhyme_with]

        def wnear(w1, w2):

            near = 0

            if len(w1) == 0 or len(w2) == 0:
                return 0

            for i in range(min([len(w1), len(w2)])):

                a = w1[len(w1) - i - 1]
                b = w2[len(w2) - i - 1]

                if a != b:
                    break
                else:
                    near += 1

            return near

        for title in titles:

            title["VOTE"] = wnear(title["LAST_WORD"], rhyme_with)

        titles = sorted(titles, key=operator.itemgetter("VOTE"), reverse=True)

        return titles
