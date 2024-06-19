import logging
import traceback
from pathlib import Path
from shutil import rmtree

from polaris.runs.scenario_file import (
    apply_modification,
    get_desired_output_dir,
    find_next_available_filename,
)
from polaris.utils.cmd_runner import run_cmd, no_printer
from polaris.utils.logging_utils import function_logging
from retry.api import retry_call


def do_nothing(*args, **kwargs):
    pass


@function_logging("  Running Polaris")
def run(
    project_dir: Path,
    polaris_exe: Path,
    base_scenario_file: str,
    scenario_modifiers,
    threads,
    printer=no_printer,
    clean_output_folder=True,
    crash_handler=do_nothing,
    run_command=run_cmd,
    num_retries=1,
):
    base_scenario_file = str(project_dir / base_scenario_file)
    report_scenario_mods(scenario_modifiers, base_scenario_file)
    scenario_file = apply_modification(base_scenario_file, scenario_modifiers)

    # Figure out exactly what the expected output dir is
    output_dir = get_desired_output_dir(scenario_file, project_dir)
    if not clean_output_folder:
        output_dir = find_next_available_filename(output_dir)

    cmd = [polaris_exe, scenario_file, str(threads)]
    logging.info(f"      exe: {polaris_exe}")
    logging.info(f"     arg1: {scenario_file}")
    logging.info(f"     arg2: {threads}")
    logging.info(f"      dir: {project_dir}")

    buf = []
    try:
        # make sure that the directory we are targeting is removed (in case this our previous attempt failed)
        def clean_output_and_run():
            buf = []  # reset the buffer
            if output_dir.exists():
                rmtree(output_dir)
            run_command(cmd, project_dir, printer, stderr_buf=buf)

        # Try running N+1 times
        retry_call(clean_output_and_run, logger=logging, tries=num_retries + 1)

        # If after all that the finished flag still doesn't exist... throw our hands up and quit
        if not (output_dir / "finished").exists():
            raise RuntimeError(
                "This should never happen: POLARIS ran to completion, returned a successful error code but did not "
                f"generate a 'finished' file in the output director ({output_dir})"
            )

    except RuntimeError as e:
        try:
            crash_handler(output_dir, buf)
        except:
            print("Error while running crash handler")
            tb = traceback.format_exc()
            print(tb, flush=True)

        log_file = output_dir / "log" / "polaris_progress.log"
        if log_file.exists():
            print(f"POLARIS crashed, check logs in {log_file}")
            with open(log_file, "r") as f:
                for l in f.readlines()[-20:]:
                    print(l.strip())
        else:
            print(f"POLARIS crashed and log file [{log_file}] wasn't yet created")
            print(f"stdout {buf}")
        raise e

    return output_dir, scenario_file


def report_scenario_mods(mods, scenario_file):
    logging.info(f"  The following modifications will be applied to {scenario_file}:")
    pad_len = max([len(k.split(".")[-1]) for k in mods.keys()])
    for k, v in mods.items():
        k = k.split(".")[-1]
        logging.info(f"    {k:<{pad_len}} : {v}")
