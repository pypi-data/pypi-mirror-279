import importlib.util as iutil

inside_qgis = iutil.find_spec("qgis") is not None
