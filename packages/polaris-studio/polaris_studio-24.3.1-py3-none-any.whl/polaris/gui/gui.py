import sys
from typing import Dict

from polaris.utils.env_utils import is_on_ci
from polaris.utils.environment import inside_qgis
from polaris.utils.optional_deps import check_dependency


class GUI:
    def __init__(self, polaris_project):
        self.__project = polaris_project
        self._data: Dict[str, dict]

    def demand_comparison(self):
        check_dependency("PyQt5")
        from PyQt5 import QtWidgets
        from .compare_demand_dialog import CompareDemandDialog

        app = None
        if not inside_qgis and not is_on_ci():
            app = QtWidgets.QApplication(sys.argv)

        dlg2 = CompareDemandDialog(polaris_project=self.__project)
        dlg2.show()
        self._data = dlg2.data
        if app is not None:
            sys.exit(app.exec_())
