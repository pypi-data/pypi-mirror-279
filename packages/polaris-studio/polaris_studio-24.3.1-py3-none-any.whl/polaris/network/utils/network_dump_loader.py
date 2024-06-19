from os import PathLike
from os.path import join
from pathlib import Path

from polaris.utils.signals import SIGNAL
from .worker_thread import WorkerThread


class LoadNetworkDump(WorkerThread):
    loading = SIGNAL(object)

    def __init__(self, folder_name: PathLike, jumpstart=False):
        WorkerThread.__init__(self, None)
        self.jumpstart = jumpstart
        self.folder_name = folder_name
        self.network_file = Path(join(self.folder_name, "polaris_network.sqlite"))

    def doWork(self):
        """Alias for execute"""
        from polaris.project.project_restorer import create_network_db_from_csv

        create_network_db_from_csv(self.network_file, self.folder_name, self.loading, False, self.jumpstart)
        self.loading.emit(["finished_dumploading_procedure"])
