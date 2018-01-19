from unittest import TestCase

from helpers.data_version_helper import IncrementalDataVersion


class TestIncrementalDataVersion(TestCase):

    def _clbk(self, notify):
        self._notifiedN += 1

    def setUp(self):

        self._notifiedN = 0
        self._idv = IncrementalDataVersion(initialCount=1)
        self._idv.getVersionChangedEventManager().add_listener(self._clbk)

    def test_notifyVersionChanged(self):

        self._idv.notifyNewVersion()

        self.assertEqual(2,self._idv.getVersion())

    def test_versionChangedEventWorks(self):

        for i in range(10):
            self._idv.notifyNewVersion()

        self.assertEqual(11, self._idv.getVersion())
        self.assertEqual(10, self._notifiedN)



