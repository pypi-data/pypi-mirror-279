import shutil
import sys
from os.path import join, isdir
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

from polaris.network.checker.supply_checker import SupplyChecker
from polaris.project.project_restorer import restore_project_from_csv
from polaris.utils.database.db_utils import read_and_close


def critical_network_tests(city: str, model_text_folder: str, model_dir=None):
    model_dir = model_dir or join(gettempdir(), uuid4().hex)

    restore_project_from_csv(model_dir, model_text_folder, city, overwrite=True)
    shutil.copytree(Path(model_text_folder) / "supply", Path(model_dir) / "supply", dirs_exist_ok=True)

    if isdir(Path(model_text_folder) / "demand"):
        shutil.copytree(Path(model_text_folder) / "demand", Path(model_dir) / "demand", dirs_exist_ok=True)

    supply_name = Path(join(model_dir, f"{city}-Supply.sqlite"))

    chckr = SupplyChecker(supply_name)

    chckr.critical()
    with read_and_close(supply_name) as conn:
        pending_edits = sum(conn.execute("""SELECT count(*) FROM "Editing_Table" where checked=0;""").fetchone())
    if pending_edits > 0:
        chckr.errors.append(f"There {pending_edits:,} are non-resolved issues in the Editing Table")

    print(chckr.errors)
    assert len(chckr.errors) == 0


if __name__ == "__main__":
    critical_network_tests(sys.argv[1], sys.argv[2])
