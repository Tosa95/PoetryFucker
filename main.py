from db_facade import DBFacade
from language.rhymer import Rhymer
from language.syllables import Syllabler
from web.app import start_web_server

dbf = DBFacade('data/phtitles.sqldb')
rhy = Rhymer(dbf,Syllabler())

start_web_server(rhy)