import traceback
from argparse import ArgumentError
from os.path import exists
from pathlib import Path
from shutil import which

from polaris.runs.scenario_file import apply_modification
from polaris.utils.cmd_runner import run_cmd
from polaris.utils.dir_utils import mkdir_p


def clone_and_build(
    model_dir=None, city=None, db_name=None, overwrite=False, inplace=False, branch="main", git_dir=None
):
    if not city:
        raise ArgumentError("Must provide city")

    from polaris.project.project_restorer import restore_project_from_csv

    db_name = db_name or city
    overwrite = overwrite or inplace  # inplace forces overwrite to true
    git_dir = Path(git_dir) if git_dir else Path(model_dir) / city / "git"
    build_dir = git_dir if inplace else Path(model_dir) / city / "built"

    ensure_updated_model(git_dir, city, branch)
    if not overwrite and exists(build_dir / f"{db_name}-Demand.sqlite"):
        print("Skipping build as files exist and overwrite = False")
    else:
        try:
            restore_project_from_csv(build_dir, git_dir, db_name, overwrite)
        except Exception:
            traceback.print_exc()

    # Make sure that the scenario file reflects our chosen db_name
    scenario_file = build_dir / "scenario_abm.json"
    apply_modification(scenario_file, {"database_name": db_name, "input_result_database_name": db_name}, scenario_file)
    return build_dir


def ensure_updated_model(git_dir, city, branch):
    if exists(git_dir / ".git"):
        run_cmd([which("git"), "checkout", branch], git_dir)
        run_cmd([which("git"), "pull"], git_dir)
    else:
        mkdir_p(git_dir)
        run_cmd(
            [
                which("git"),
                "clone",
                "--branch",
                branch,
                f"https://gitlab:GM9KMJJJfyEBrBSQMaX5@git-out.gss.anl.gov/polaris/models/{city}.git",
                str(git_dir),
            ],
            ".",
        )
