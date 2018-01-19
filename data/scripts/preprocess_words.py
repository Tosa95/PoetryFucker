import json
import os

DATA_DIRECTORY = ".."

WORD_LIST_FILE = os.path.join(DATA_DIRECTORY, "660000_parole_italiane.txt")
JSON_WORD_LIST_FILE = os.path.join(DATA_DIRECTORY, "italian_words.json")

with open(WORD_LIST_FILE,'r') as f:
    words = f.readlines()

words = [w.lower().strip('\n').replace("'",'').replace('&','') for w in words
         if w.strip('\n').isalpha()]

words = sorted(words)

with open(JSON_WORD_LIST_FILE, 'w') as f:
    f.write(json.dumps(words,indent=4,sort_keys=True))


