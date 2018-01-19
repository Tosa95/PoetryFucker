from unittest import TestCase

from language.language_identifier import load_dictionary, DictionaryLanguageIdentifier


class TestDictionaryLanguageIdentifier(TestCase):



    def setUp(self):
        super(TestDictionaryLanguageIdentifier, self).setUp()

        dictionary = load_dictionary({"english":"../data/english_words.json",
                                      "italian":"../data/italian_words.json"})

        self._li = DictionaryLanguageIdentifier(dictionary)


    def test_identify_lang(self):

        self.assertEqual(self._li.identify_lang("hi"), "unknown")
        self.assertEqual(self._li.identify_lang("ciao"), "unknown")
        self.assertEqual(self._li.identify_lang("COME STAI?"), "italian")
        self.assertEqual(self._li.identify_lang("HOW ARE YOU?"), "english")
