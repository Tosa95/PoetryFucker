from unittest import TestCase

from db_facade import DBFacade


class TestDBFacade(TestCase):



    def setUp(self):
        super(TestDBFacade, self).setUp()

        self._dbf = DBFacade('data/phtitles.sqldb')

    def test_get_title_by_id(self):

        print self._dbf.get_title_by_id(12)["TITLE"]
