from abc import ABCMeta, abstractmethod

from helpers.observer_helper import BasicObservableHelper, ObservableExternalInterface


class DataVersion(object):

    __metaclass__ = ABCMeta

    def __init__(self):
        self._versionChangedNotifier = BasicObservableHelper()

    def getVersionChangedEventManager(self):
        return ObservableExternalInterface(self._versionChangedNotifier)

    @abstractmethod
    def getVersion(self):
        """
        Returns the version of data
        :return: The version
        """
        pass


class IncrementalDataVersion(DataVersion):



    def __init__(self, initialCount=1):
        super(IncrementalDataVersion, self).__init__()
        self._count = initialCount


    def getVersion(self):
        return self._count

    def notifyNewVersion(self):
        self._count += 1
        self._versionChangedNotifier.notify(self)


