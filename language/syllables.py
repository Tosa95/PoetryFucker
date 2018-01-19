# coding=utf-8
import re

VOWELS = "aeiou"
CONSONANTS = "bcdfghlmnpqrstvz"
DOUBLE_C = [c+c for c in CONSONANTS]
DIPHTHONG = ["ia","ie","io","iu","ua","ue","uo","ui","ai","ei","oi","ui","au","eu"]
#DIPHTHONG = ["ai","ei","oi","au","eu"]
TRIPHTHONG = ["iai","iei","ioi","uai","uei","uoi","iuo","uia"]
TO_BE_DIVIDED = ["cn","lm","rc","bd","mb","mn","ld","ng","nd","nd","tm","cq","nz","nt","ns","rd","mp","rn","lv","lp",
                 "lt","rz","rt","rm","nf","lg","rb","lc","nv","lz","rl","rg","rs","rv","lc","nc","rf","rp","lb"] + DOUBLE_C
CANT_BE_DIVIDED = ["bl","cl","dl","fl","gl","pl","tl","vl","br","cr","dr","fr","gr","pr","tr","vr"] + DIPHTHONG +\
                  TRIPHTHONG



VOWEL_SYMBOL = r'\v'
CONSONANT_SYMBOL = r'\c'

class Syllabler:

    def __init__(self):

        pass

    def preprocess_text(self, title):

        chars_to_remove = u"!?$().,:;-_\/&%£"

        for char_to_remove in chars_to_remove:
            title = title.replace(char_to_remove, '')

        return title.lower()

    def is_vocal(self,character):

        return character in VOWELS

    def is_consonant(self,character):

        return character.isalpha() and not self.is_vocal(character)

    def expand_regex(self,compact_regex):

        return compact_regex.replace(CONSONANT_SYMBOL,"[" + CONSONANTS + "]")\
                .replace(VOWEL_SYMBOL,"[" + VOWELS + "]")

    def cuts_a_diphthong(self,word,syllable_start,syllable_end):

        if syllable_end >= len(word)-1:
            return False

        else:

            piece = word[syllable_end:syllable_end+2]

            return piece in DIPHTHONG

    def cuts_a_triphthong(self,word,syllable_start,syllable_end):

        if syllable_end >= len(word)-2:
            return False

        else:

            piece = word[syllable_end:syllable_end+3]

            return piece in TRIPHTHONG

    def cuts_one(self,word,syllable_start,syllable_end,pieces):

        for piece in pieces:

            for i in range(1,len(piece)):

                after = len(piece) - i
                before = len(piece) - after

                if len(word[syllable_end+1:])>=after and len(word[:syllable_end+1])>=before and syllable_end-before+1 >= syllable_start:
                    start = syllable_end-i+1
                    word_piece = word[start:start+len(piece)]
                    if word_piece == piece:
                        return True

        return False

    def cuts_double(self,word,syllable_start,syllable_end):

        if syllable_end >= len(word)-1:
            return False

        else:

            piece = word[syllable_end:syllable_end+2]

            return piece[0] == piece[1]

    def must_be_a_syllable(self,word,syllable_start,syllable_end):

        if self.is_consonant(word[syllable_end]) and word[syllable_end] != 's' and len(word) - syllable_end - 1 >= 2:

            if self.is_consonant(word[syllable_end+1]) and  self.is_consonant(word[syllable_end+2]):
                return True

        if syllable_start == 0 and syllable_end-syllable_start==0 and len(word) >= 3 and self.is_vocal(word[0])\
                and self.is_consonant(word[1]) and self.is_vocal(word[2]):

            return True

        if len(word[syllable_end:])>=3:

            piece = word[syllable_end:syllable_end+3]

            regex = self.expand_regex(r"^\v\v\v$")

            if re.match(regex,piece) is not None and piece not in TRIPHTHONG:

                return True

        #if self.cuts_double(word,syllable_start,syllable_end):

        #    return True

        #a = word[syllable_end:syllable_end+2]

        #if len(word[syllable_end:])>=2 and word[syllable_end:syllable_end+2] in TO_BE_DIVIDED:

        #    return True

        if self.cuts_one(word,syllable_start,syllable_end,TO_BE_DIVIDED):
            return True

        return False

    def can_be_a_syllable(self,word,syllable_start,syllable_end):

        syllable = word[syllable_start:syllable_end+1]

        consonant_re = self.expand_regex(r"^\c*$")

        # If only consonants cant be a syllable
        if re.match(consonant_re,syllable) is not None:
            return False

        #if syllable_start == 0 and syllable_end-syllable_start == 0 and len(word) >= 3 and self.is_vocal(word[0]) \
        #        and self.is_consonant(word[1]) and self.is_consonant(word[2]):
        #    return False

        # If it cuts a diphthong can't be a syllable
        #if self.cuts_a_diphthong(word,syllable_start,syllable_end):

        #    return False

        # If it cuts a triphthong can't be a syllable
        #if self.cuts_a_triphthong(word,syllable_start,syllable_end):

        #    return False

        if self.cuts_one(word,syllable_start,syllable_end,CANT_BE_DIVIDED):
            return False

        # If adding up to 4 consonants
        for i in range(1, 5):

            if len(word) - syllable_end - 1 >= i:

                sy = word[syllable_end+1:syllable_end+i+1]

                if re.match(consonant_re, sy) and self.must_be_a_syllable(word,syllable_start,syllable_end+i):
                    return False

        #if len(word) - syllable_end - 1 >= 3 and self.is_consonant(word[syllable_end+1]):

        #    if self.is_consonant(word[syllable_end+2]) and  self.is_consonant(word[syllable_end+3]):
        #        return False

        return True

    def syllables(self,word):

        res = ""

        curr_start = 0
        curr_end = 0

        while curr_end<len(word):

            curr = word[curr_start:curr_end+1]

            if self.must_be_a_syllable(word,curr_start,curr_end) or \
                self.can_be_a_syllable(word, curr_start, curr_end):

                res += curr+"-"

                curr_end += 1
                curr_start = curr_end


            else:

                curr_end += 1

        res += word[curr_start:curr_end]

        if len(res)>0 and res[-1] == '-':

            res = res[:-1]

        return res
