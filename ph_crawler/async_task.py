from abc import ABCMeta, abstractmethod
from threading import Thread

from helpers.observer_helper import ThreadedObservableHelper, ObservableExternalInterface


class UnableToStartExecutionException(Exception):
    pass


class WorkerThreadNotStarted(Exception):
    pass


class AsyncTask:
    """
    Represents an async task
    """
    __metaclass__ = ABCMeta

    def __init__(self, autoStopNotifiers=True, abortIfSubExecutorFails=True):
        """
        Initializes the executor
        :param autoStopNotifiers: True: notifiers are stopped automatically at the end of the execution,
        False: tasks must be stopped manually
        """
        self._progressChangedNotifier = ThreadedObservableHelper()
        self._executionCompletedNotifier = ThreadedObservableHelper()
        self._errorRaisedNotifier = ThreadedObservableHelper()
        self._abortedNotifier = ThreadedObservableHelper()
        self._progress = 0
        self._taskName = ""
        self._mustBeAborted = False
        self._workerThread = None
        self._doneFlag = False
        self._abortedFlag = False
        self._autoStopNotifiers = autoStopNotifiers
        self._notifiersStarted = False
        self._abortIfSubExecutorFails = abortIfSubExecutorFails

    def _startNotifiers(self):
        self._progressChangedNotifier.startNotifierThread()
        self._executionCompletedNotifier.startNotifierThread()
        self._errorRaisedNotifier.startNotifierThread()
        self._abortedNotifier.startNotifierThread()

        self._notifiersStarted = True

    def getProgressChangeEventManager(self):
        """
        Returns an interface for adding and removing listeners to/from the progressChanged event 
        :return: The interface
        """
        return ObservableExternalInterface(self._progressChangedNotifier)

    def getExecutionCompletedEventManager(self):
        """
        Returns an interface for adding and removing listeners to/from the executionCompleted event 
        :return: The interface
        """
        return ObservableExternalInterface(self._executionCompletedNotifier)

    def getErrorRaisedEventManager(self):
        """
        Returns an interface for adding and removing listeners to/from the errorRaised event 
        :return: The interface
        """
        return ObservableExternalInterface(self._errorRaisedNotifier)

    def getAbortedEventManager(self):
        """
        Returns an interface for adding and removing listeners to/from the aborted event 
        :return: The interface
        """
        return ObservableExternalInterface(self._abortedNotifier)

    def _setProgress(self, progress):
        """
        Changes the progress of the task being executed by the executor
        :param progress: The progress, a float between 0 and 100
        """
        # print "Progress set %.2f --------------------------------" % progress

        if progress > 100.0:
            progress = 100.0

        self._progress = progress
        self._progressChangedNotifier.notify(self)

    def _setTaskName(self, taskName):
        """
        Sets the current task name to the one provided
        :param taskName: The name to be set for the current task 
        """
        self._taskName = taskName
        self._progressChangedNotifier.notify(self)

    def _done(self):
        """
        Called when the task is completed
        """
        self._doneFlag = True
        self._executionCompletedNotifier.notify(self)

    def _aborted(self):
        """
        Called when the task ends by abortion 
        """
        self._abortedFlag = True
        self._abortedNotifier.notify(self)

    def getProgress(self):
        """
        Returns the current progress
        :return: The current progress
        """
        return self._progress

    def getTaskName(self):
        """
        Returns the name of the current task
        :return: The name of the current task
        """
        return self._taskName

    def isDone(self):
        return self._doneFlag

    def isAborted(self):
        return self._abortedFlag

    def stopNotifiers(self):
        """
        Stops all the notifiers used by the object. 

        If a child class adds more notifiers, it should override this method in order to let them be stopped
        at the right time
        """
        self._executionCompletedNotifier.stop(wait=False)
        self._progressChangedNotifier.stop(wait=False)
        self._errorRaisedNotifier.stop(wait=False)
        self._abortedNotifier.stop(wait=False)

        self._executionCompletedNotifier.join()
        self._progressChangedNotifier.join()
        self._errorRaisedNotifier.join()
        self._abortedNotifier.join()

        self._notifiersStarted = False

    def abort(self, timeout=None):
        """
        Aborts the execution
        :param timeout: The maximum amount of time to wait for (waits forever if None)
        :return: True: process terminated, False: abortion process begun, but not yet terminated
        """
        self._mustBeAborted = True

        res = self.waitForTermination(timeout)

        return res

    def waitForTermination(self, timeout=None):
        """
        Waits for the task to be completed
        :param timeout: The maximum amount of time to wait for (waits forever if None)
        :return: True: the process terminated, False: the process is not terminated
        """

        if (self._workerThread is None):
            raise WorkerThreadNotStarted("Unable to wait for termination on a not running thread")

        if timeout is None:
            self._workerThread.join()
            return True
        else:
            self._workerThread.join(timeout)
            if self._workerThread.isAlive():
                return False
            else:
                return True

    @abstractmethod
    def _worker(self, args):
        """
        Used to implement a template method design pattern. This method has to be overridden by child classes
        in order to define their behaviour
        :param args: A tuple containing the parameters for the task
        """
        pass

    def _exceptionHandlingWorker(self, args):
        """
        Wrapper for the _worker template method.

        It handles task's exc, done and abortion notify, and automatic notifiers stop

        :param args: A tuple containing the parameters for the task
        """
        self._doneFlag = False
        self._abortedFlag = False
        if not self._notifiersStarted:
            self._startNotifiers()

        try:
            self._worker(args)
        except Exception as ex:
            # print "Exc"
            self._errorRaisedNotifier.notify(ex)
        finally:
            # print "Finally"

            if not self._mustBeAborted:
                self._done()
            else:
                self._aborted()

            # print "Before stop notifiers"
            if self._autoStopNotifiers:
                try:
                    self.stopNotifiers()
                except Exception as ex:
                    print ex


                    # print "ExcWorkerDone"

    def _startWorkerThread(self, group=None, name=None, args=None):
        """
        Starts the worker thread in order to let the task be executed asynchronously
        :param group: The thread group
        :param name: The thread name
        :param args: A tuple containing the parameters for the task
        :return: 
        """

        if (self._workerThread is not None) and self._workerThread.isAlive():
            raise UnableToStartExecutionException("Another task is already being executed")

        self._workerThread = Thread(group=group, target=self._exceptionHandlingWorker, name=name,
                                    args=((args,) if args is not None else ()))

        self._workerThread.start()

    def _errorRedirection(self, ex):
        """
        Callback used to handle error redirection from sub-executors to main executor
        :param ex: The exception raised
        """
        self._errorRaisedNotifier.notify(ex)

        self._mustBeAborted = True

    def _redirectErrors(self, other):
        """
        Activates the error redirection from other to self
        :param other: An executor of which we want errors to be redirected to the error notifier of self
        """
        other.getErrorRaisedEventManager().add_listener(self._errorRedirection)
