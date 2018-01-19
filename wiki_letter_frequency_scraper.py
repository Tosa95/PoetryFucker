import os

import bs4
import requests
import time
import json
from bs4 import BeautifulSoup

page = requests.get("https://en.m.wikipedia.org/wiki/Letter_frequency")

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find_all(class_="wikitable")[2]

data = dict()
lnames = list()

intestazione = [x for x in list(table.children)[0].children if type(x) == bs4.element.Tag]

datarows = list(table.children)[1:]

for tag in intestazione[1:]:

    lname = tag.text.split(' ')[0].lower()

    data[lname] = dict()

    lnames.append(lname)

    #print lname

for datarow in datarows:

    row = [x for x in list(datarow.children) if type(x) == bs4.element.Tag]

    character = row[0].text

    for (perc,index) in zip(row[1:], range(0,len(lnames)-1)):

        num = float(perc.text.strip('%*'))/100.0
        data[lnames[index]][character] = num
        print lnames[index]


with open("letter_lang_data",'w') as f:

    f.write(json.dumps(data))

print json.dumps(data)



#print lnames

