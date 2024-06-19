import shutil
import tempfile

from polaris.utils.env_utils import is_windows


def TempModel(model_name):
    fldr = f"C:/temp_container/{model_name}" if is_windows() else f"/tmp/{model_name}"
    new_fldr = tempfile.mkdtemp()
    shutil.copytree(fldr, new_fldr, dirs_exist_ok=True)
    return new_fldr
