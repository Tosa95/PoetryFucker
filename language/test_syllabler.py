from unittest import TestCase

import re

from db_facade import DBFacade
from language.syllables import Syllabler


class TestSyllabler(TestCase):



    def setUp(self):
        super(TestSyllabler, self).setUp()

        self._syllabler = Syllabler()

    def test_is_vocal(self):
        self.assertTrue(self._syllabler.is_vocal('a'))
        self.assertFalse(self._syllabler.is_vocal('d'))

    def test_is_consonant(self):
        self.assertTrue(self._syllabler.is_consonant('d'))
        self.assertFalse(self._syllabler.is_consonant('e'))

    def test_expands_regex(self):
        self.assertEqual(self._syllabler.expand_regex(r"^\v+$"),"^[aeiou]+$")
        self.assertEqual(self._syllabler.expand_regex(r"^\c*$"), "^[bcdfghlmnpqrstvz]*$")
        self.assertEqual(self._syllabler.expand_regex(r"^\v+\c*$"), "^[aeiou]+[bcdfghlmnpqrstvz]*$")

        print(re.match(self._syllabler.expand_regex(r"^\c*$"),"qqqsd") != None)
        print(re.match(self._syllabler.expand_regex(r"^\c*$"), "qqqaa") != None)

    def test_cuts_a_diphthong(self):
        self.assertTrue(self._syllabler.cuts_a_diphthong("provai",3,4))
        self.assertFalse(self._syllabler.cuts_a_diphthong("provai", 0, 3))
        self.assertTrue(self._syllabler.cuts_a_diphthong("guano",0,1))
        self.assertFalse(self._syllabler.cuts_a_diphthong("guano", 0, 2))
        self.assertFalse(self._syllabler.cuts_a_diphthong("guano", 0, 4))

    def test_cuts_a_tripthong(self):
        self.assertTrue(self._syllabler.cuts_a_triphthong("aiuola",0,1))
        self.assertFalse(self._syllabler.cuts_a_triphthong("aiuola", 0, 0))
        self.assertFalse(self._syllabler.cuts_a_triphthong("aiuola", 1, 3))
        self.assertFalse(self._syllabler.cuts_a_triphthong("aiuola", 4, 4))

    def test_cuts_double(self):
        self.assertTrue(self._syllabler.cuts_double("rottame", 0, 2))
        self.assertFalse(self._syllabler.cuts_double("rottame", 0, 3))

    def test_syllables(self):
        print self._syllabler.syllables("rottame")
        print self._syllabler.syllables("controllo")
        print self._syllabler.syllables("ventricolo")
        print self._syllabler.syllables("scaltro")
        print self._syllabler.syllables("pinguino")
        print self._syllabler.syllables("criceto")
        print self._syllabler.syllables("gatto")
        print self._syllabler.syllables("polmone")
        print self._syllabler.syllables("stronzo")
        print self._syllabler.syllables("puttana")
        print self._syllabler.syllables("atletico")
        print self._syllabler.syllables("anale")
        print self._syllabler.syllables("troia")
        print self._syllabler.syllables("onestissimo")
        print self._syllabler.syllables("tagliarla")
        print self._syllabler.syllables("auguro")
        print self._syllabler.syllables("incasserei")
        print self._syllabler.syllables("ospiteremmo")
        print self._syllabler.syllables("istituiscono")
        print self._syllabler.syllables("aprirgli")
        print self._syllabler.syllables("sospiro")

        dbf = DBFacade("../data/db.sqldb")



        words = dbf.get_random_words(100)

        correct = 0
        total = 0

        for word in words:

            w = word[0]
            s = word[1]

            if self._syllabler.syllables(w) == s:

                correct += 1

            else:

                print "Wrong: " + w + " Exact: " + s + " Given: " + self._syllabler.syllables(w)

            total += 1

        print (float(correct)/float(total))*100