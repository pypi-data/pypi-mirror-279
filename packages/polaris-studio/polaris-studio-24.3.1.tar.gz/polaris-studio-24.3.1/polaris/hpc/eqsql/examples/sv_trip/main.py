import datetime
import json
import logging
import os
import subprocess
import sys
import traceback
from pathlib import Path
from socket import gethostname
from tempfile import TemporaryDirectory

from gpra_config import GPRAConfig

import pandas as pd
from polaris.hpc.eqsql.task_container import TaskContainer
from polaris.runs.polaris_inputs import PolarisInputs
from polaris.runs.scenario_utils import extract_iteration
from polaris.runs.sv_trip import export_sv_trip
from polaris.utils.copy_utils import magic_copy
from polaris.utils.dir_utils import mkdir_p, slow_rmtree
from polaris.utils.env_utils import get_data_root
from polaris.utils.logging_utils import function_logging


def main(payload):
    task_container = TaskContainer.from_env(payload)
    task_container.log("Got Payload")
    try:
        install_latest_svtrip()
        do_the_run(task_container)
    except Exception:
        tb = traceback.format_exc()
        task_container.log(tb)
        print(tb, flush=True)
        exit(1)


def do_the_run(task_container):
    run_id = task_container.payload["run-id"]
    gpra_config = GPRAConfig.from_run_id(run_id)
    model_dir_name = f"{run_id}_{gpra_config.city}"

    def remote_get_best_iteration(remote_dir):
        tmp_dir = get_data_root() / "tmp"
        mkdir_p(tmp_dir)
        gap_file = remote_dir / "gap_calculations.csv"
        magic_copy(gap_file, tmp_dir / gap_file.name, recursive=False)
        gaps = pd.read_csv(tmp_dir / gap_file.name).set_index("directory")
        iter_name = gaps.tail(5)["relative_gap_min0"].idxmin()
        return remote_dir / iter_name

    # find the results on the file server and determine the best iteration
    run_dir = Path(task_container.payload["get-results-from-here"]) / model_dir_name
    #  model_src_dir = get_best_iteration(ConvergenceConfig(data_dir=run_dir, db_name=gpra_config.city))
    model_src_dir = remote_get_best_iteration(run_dir)

    # setup logging
    model_dir = Path(get_data_root()) / "sv_trip" / model_dir_name / model_src_dir.stem
    # setup_logging(Path(task_container.payload["put-logs-here"]) / model_dir_name, model_dir)
    setup_logging(model_dir)

    # copy best iteration to local
    if model_dir.exists():
        logging.info(f"Cleaning {model_dir}")
        slow_rmtree(model_dir)
    # logging.info(f"Copying {model_src_dir} -> {model_dir}")
    # shutil.copytree(model_src_dir, model_dir)
    magic_copy(model_src_dir, model_dir)
    task_container.log("SVTrip - Finished copying down files")

    extract_iteration(model_dir, gpra_config.db_name())
    export_sv_trip(PolarisInputs.from_dir(model_dir, gpra_config.db_name()))
    task_container.log("SVTrip - Finished exporting files")
    copy_sv_trip_files(task_container, run_id, gpra_config.city, gpra_config.db_name(), model_dir)
    task_container.log("SVTrip - Finished copying up files")
    slow_rmtree(model_dir)
    task_container.log("SVTrip - Finished deleting local files")


def setup_logging(local_dir):
    mkdir_p(local_dir)
    date_stamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
    handler_f1 = logging.FileHandler(os.path.join(local_dir, f"sv_trip_runner_{date_stamp}_{gethostname()}.log"))
    handler_std = logging.StreamHandler(sys.stdout)
    logging.basicConfig(
        handlers=[handler_std, handler_f1], force=True, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def install_latest_svtrip():
    # Hack to make sure we have teh latest svtrip installed
    ci_dir = Path("/mnt/p/VMS_Software/15-CI-CD-Artifacts/Polaris")
    py_ver = f"{sys.version_info.major}{sys.version_info.minor}"
    latest_wheel = (
        f"svtrip-20221103-cp{py_ver}-cp{py_ver}-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl"
    )
    with TemporaryDirectory(dir=get_data_root() / "tmp") as tmp_dir:
        tmp_dir = Path(tmp_dir)
        magic_copy(ci_dir / "SVTrip" / "latest" / "wheels" / latest_wheel, tmp_dir / latest_wheel, recursive=False)
        cmd = f"{sys.executable} -m pip install --upgrade {tmp_dir / latest_wheel}"
        subprocess.run(cmd, shell=True, check=True)


@function_logging("  Copying SVTrip files to the Cluster file share")
def copy_sv_trip_files(task_container, run_id, city, db_name, output_dir):
    target_folders = task_container.payload["put-svtrip-results-here"]
    if isinstance(target_folders, str):
        target_folders = [target_folders]

    sv_trip_dir = output_dir / "sv_trip_outputs"
    flag_file = sv_trip_dir / "copy_finished.txt"
    flag_file.unlink(missing_ok=True)

    for folder in target_folders:
        folder = Path(folder) / f"{run_id}_{city}"

        # Copy over the demand db used in svtrip
        demand_db = f"{db_name}-Demand.sqlite"
        magic_copy(str(output_dir / demand_db), str(folder / demand_db), recursive=False)

        # Copy over the svtrip outputs
        dest_dir = folder / "sv_trip_outputs"
        magic_copy(str(sv_trip_dir), str(dest_dir))

        # Touch a flag file so that automated autonomie processing can be triggered
        flag_file.touch()
        magic_copy(str(flag_file), str(dest_dir / "copy_finished.txt"), recursive=False)
        flag_file.unlink()


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        main(json.loads(f.read()))
