class _Connector:
    """
        Base class
    """

    def __init__(self, *args):
        pass

    def connect(self):
        pass


class TToWConnector(_Connector):
    """
        Thread to Worker Connector

        connects QThread to Worker for button events
    """

    def __init__(self, thread, worker):
        super(TToWConnector, self).__init__()
        self._thread = thread
        self._worker = worker
        self.connect()

    def connect(self):
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def get_thread(self):
        return self._thread

    def get_worker(self):
        return self._worker


# class EToBConnector(_Connector):
#     def __init__(self, event, button, func):
#         super(EToBConnector, self).__init__()
#         self._event = event
#         self._button = button
#         self._func = func
#         self.connect()
#
#     def connect(self):
#         self._button.finished.connect(self._func)
#
#     def get_event(self):
#         return self._thread
#
#     def get_button(self):
#         return self._worker