"""
 Copied from AequilibraE
 Original Author:  UNKNOWN. COPIED FROM STACKOVERFLOW BUT CAN'T REMEMBER EXACTLY WHERE
 """

from polaris.utils.environment import inside_qgis

if inside_qgis:
    from PyQt5.QtCore import QThread
    from PyQt5.QtCore import pyqtSignal
else:

    class QThread:  # type: ignore
        def __init__(self, *arg):
            pass


class WorkerThread(QThread):
    if inside_qgis:
        jobFinished = pyqtSignal(object)

    def __init__(self, parentThread):
        QThread.__init__(self, parentThread)

    def run(self):
        self.running = True
        success = self.doWork()
        if inside_qgis:
            self.jobFinished.emit(success)

    def stop(self):
        self.running = False
        pass

    def doWork(self):
        "It will overloaded by the classes that subclass this"
        return True

    def cleanUp(self):
        pass
