# coding=utf-8
import json
from abc import ABCMeta, abstractmethod
from bisect import bisect_left


class LanguageIdentifier:
    __metaclass__ = ABCMeta

    @abstractmethod
    def identify_lang(self,text):
        pass


class FrequencyLanguageIdentifier(LanguageIdentifier):

    def __init__(self, lang_data):

        self._lang_data = lang_data

    def calc_relative_frequencies(self,text):

        text = text.lower()

        res = {}
        total = len(text)

        for letter in self._lang_data['italian']:
            res[letter] = 0.0

        for ch in text:

            if ch in res:

                res[ch] += 1.0/total

        return res

    def dist_lang(self,text,lang):

        rel = self.calc_relative_frequencies(text)

        lang_rel = self._lang_data[lang]

        res = 0

        for ch in lang_rel:

            res += abs(rel[ch] - lang_rel[ch])

        return res

    def identify_lang(self, text):

        langmin = ""
        min = 10000

        for lang in self._lang_data:

            dst = self.dist_lang(text,lang)

            if dst<min:
                langmin = lang
                min = dst

        return langmin

def has_word(word, lst):

    pos = bisect_left(lst,word)

    try:
        if lst[pos] == word:

            return True

        else:

            return False
    except IndexError:

        return False

def preprocess_text(title):

    chars_to_remove = u"!?$().,:;-_\/&%£"

    for char_to_remove in chars_to_remove:

        title = title.replace(char_to_remove,'')

    return title.lower()

def load_dictionary (file_dict):

    res = {}

    for lang in file_dict:

        filename = file_dict[lang]

        with open(filename,'r') as f:

            res[lang] = json.load(f)

    return res

class DictionaryLanguageIdentifier(LanguageIdentifier):

    def __init__(self, word_dict, min_words=2):

        self._word_dict = word_dict
        self._min_words = min_words

    def identify_lang(self,text):

        best_lang = "unknown"
        best_count = 0

        text = preprocess_text(text)

        words = text.split(' ')

        for lang in self._word_dict:

            count = 0

            for word in words:

                if has_word(word, self._word_dict[lang]):
                    count += 1

            if count > best_count:

                best_count = count
                best_lang = lang

        if best_count >= self._min_words:

            return best_lang

        else:

            return "unknown"


