from PyQt5.QtCore import pyqtSignal, QThread


class Thread(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(object)
    finish = pyqtSignal()

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.func(*self.args, **self.kwargs, progress_callback=self.progress.emit)
        self.result.emit(result)
        self.finish.emit()
