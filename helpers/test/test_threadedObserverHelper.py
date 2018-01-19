import unittest
from unittest import TestCase

import time

from helpers.observer_helper import ThreadedObservableHelper


class TestThreadedObserverHelper(TestCase):

    def init(self):
        self._callbackDone = False
        self._infoOK = False
        self._count = 0

    def _list(self, info):
        time.sleep(0.1)

        if info == "ciao":
            self._infoOK = True

        self._callbackDone = True

        self._count += 1

    def test_listenerCalled(self):

        self.init()

        oh = ThreadedObservableHelper()

        oh.startNotifierThread()

        oh.add_listener(self._list)

        init = time.time()

        oh.notify("ciao")

        endNotify = time.time()

        while self._callbackDone == False:
            time.sleep(0.1)


        notified = time.time()

        oh.stop()

        notifyMethodTime = (endNotify-init)
        notificationTime = (notified - init)

        self.assertTrue(notifyMethodTime < 0.005)

        self.assertTrue(notificationTime > 0.1)

        self.assertTrue(self._infoOK)

    def test_moreListernersCalled(self):

        self.init()

        oh = ThreadedObservableHelper()
        oh.startNotifierThread()

        oh.add_listener(self._list)
        oh.add_listener(self._list)
        oh.add_listener(self._list)

        oh.notify("ciao")
        oh.notify("ciao")

        time.sleep(0.7)

        oh.stop()

        self.assertEqual(6, self._count)

if __name__ == "__main__":
    unittest.main()


