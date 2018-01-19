from Queue import Queue, Empty
from abc import ABCMeta
from abc import abstractmethod
from threading import Thread

class ObservableExternalInterface(object):

    def __init__(self, observable):

        self.__observable = observable

    def add_listener (self, listener):
        self.__observable.add_listener(listener)

    def remove_listener (self, listener):
        self.__observable.remove_listener(listener)

class AbstractObservableHelper(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_listener (self, listener):
        pass

    @abstractmethod
    def remove_listener(self, listener):
        pass

    @abstractmethod
    def notify (self, info=None):
        pass


class AbstractListener(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self):
        pass

class BasicObservableHelper (AbstractObservableHelper):

    def __init__(self):
        self._listeners = []

    def add_listener(self, listener):
        self._listeners.append(listener)

    def remove_listener(self, listener):
        self._listeners.remove(listener)

    def notify(self, info=None):
        [l(info) for l in self._listeners]

class ThreadedObservableHelper (BasicObservableHelper):
    """
    Acts like a BasicObserverHelper, with the difference that listeners are called
    in a different thread so that listeners execution does not slow down the subject
    """


    def __init__(self, maxSize = 0):
        """
        Initializes the helper
        :param maxSize: The maximum event number that can be in the queue
        """
        super(ThreadedObservableHelper, self).__init__()
        self._notifyQueue = Queue(maxSize)
        self._notifier = None
        self._createNewThread()

    def _createNewThread(self):

        import inspect

        if self._notifier is not None and self._notifier.isAlive():
            self.stop()

        self._stop = False

        self._notifier = Thread(name="NotifierThread: %s" % inspect.currentframe().f_back.f_locals['self'], target=self._worker)

    def startNotifierThread(self):

        self._createNewThread()

        self._notifier.start()

    def _worker(self):
        """
        The dispatcher thread target 
        """
        while not self._stop:
            try:
                info = self._notifyQueue.get(timeout=0.03)
                [l(info) for l in self._listeners]
            except Empty:
                pass

            #print "Notifier thread done"

    def stop(self, wait=True):
        """
        Stops the dispatcher thread and joins it
        """
        while not self._notifyQueue.empty():
            pass

        self._stop = True

        if wait:
            self.join()

    def join(self):

        self._notifier.join()

    def notify(self, info=None):

        self._notifyQueue.put(info)

