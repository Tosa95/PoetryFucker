import json
from unittest import TestCase

from language.language_identifier import FrequencyLanguageIdentifier


class TestLanguageIdentifier(TestCase):



    def setUp(self):
        super(TestLanguageIdentifier, self).setUp()

        data = {}

        with open("letter_lang_data","r") as f:

            data = json.loads(f.read())

        data = {k:v for k,v in data.iteritems() if k == 'italian' or k == 'english'}

        self._li = FrequencyLanguageIdentifier(data)

    def test_calc_relative_frequencies(self):

        res = self._li.calc_relative_frequencies("ciao")

        sum = 0

        for ch in res:

            sum += res[ch]

        self.assertAlmostEqual(sum, 1, delta=0.0001)

        self.assertAlmostEqual(res['c'], 1.0/4.0, delta=0.0001)
        self.assertAlmostEqual(res['i'], 1.0 / 4.0, delta=0.0001)
        self.assertAlmostEqual(res['a'], 1.0 / 4.0, delta=0.0001)
        self.assertAlmostEqual(res['o'], 1.0 / 4.0, delta=0.0001)

    def test_identify_lang(self):

        self.assertEqual(self._li.identify_lang("hi"), "english")
        self.assertEqual(self._li.identify_lang("ciao"), "italian")
        self.assertEqual(self._li.identify_lang("COME STAI?"), "italian")
        self.assertEqual(self._li.identify_lang("HOW ARE YOU?"), "english")
