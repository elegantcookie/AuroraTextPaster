class _Connector:
    """ Базовый класс """

    def __init__(self, *args):
        pass

    def connect(self):
        pass


class TToWConnector(_Connector):
    """ Соединитель потока и воркера """

    def __init__(self, thread, worker):
        super(TToWConnector, self).__init__()
        self._thread = thread
        self._worker = worker
        self.connect()

    def connect(self):
        """ Соединяет и запускает поток на воркере """
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

