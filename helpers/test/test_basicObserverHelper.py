import unittest
from unittest import TestCase
import helpers.observer_helper


class TestBasicObserverHelper(TestCase):


    def _notify(self, info):
        self._a = self._a + 1

    def test_add_one_listener_notify(self):

        self._a = 0

        help = helpers.observer_helper.BasicObservableHelper()
        list = self._notify
        help.add_listener(list)



        help.notify()



        self.assertEqual(self._a, 1)

    def test_add_two_listener_notify_two_times(self):
        self._a = 0

        help = helpers.observer_helper.BasicObservableHelper()

        help.add_listener(self._notify)
        help.add_listener(self._notify)



        help.notify()



        self.assertEqual(self._a, 2)

if __name__ == "__main__":
    unittest.main()