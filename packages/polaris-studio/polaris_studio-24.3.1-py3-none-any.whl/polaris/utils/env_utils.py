import os
from pathlib import Path
from socket import gethostname

from enum import IntEnum


def is_windows() -> bool:
    return os.name == "nt"


def is_not_windows() -> bool:
    return os.name != "nt"


def is_on_ci() -> bool:
    # CI_COMMIT_REF_NAME is defined for all GitLab runner environments, CI for GitHub Actions environments
    return env_var_defined("CI_COMMIT_REF_NAME") or env_var_defined("CI")


def env_var_defined(x) -> bool:
    return os.environ.get(x) is not None


def should_run_integration_tests() -> bool:
    if not is_on_ci():
        return True  # always allow tests to run locally

    # Otherwise, only run on main (or testing branches) which are executed from linux
    integration_branches = ["main", "fds/integration_test"]
    return is_not_windows() and any(branch == os.environ["CI_COMMIT_REF_NAME"] for branch in integration_branches)


class WhereAmI(IntEnum):
    DESKTOP = 0
    WSL_CLUSTER = 1
    CROSSOVER_CLUSTER = 2
    BEBOP_CLUSTER = 3
    IMPROV_CLUSTER = 4
    HPC_CLUSTER = 5


def where_am_i_running(clue=None) -> WhereAmI:
    clue = clue or gethostname()
    if "crossover" in clue or "xover" in clue:
        return WhereAmI.CROSSOVER_CLUSTER
    if "bebop" in clue or "bdw" in clue:
        return WhereAmI.BEBOP_CLUSTER
    if "ilogin" in clue or "improv" in clue or "i0" in clue or "i1" in clue or "i2" in clue:
        return WhereAmI.IMPROV_CLUSTER
    if "VMS-C" in clue:
        return WhereAmI.WSL_CLUSTER
    if "VMS-HPC" in clue:
        return WhereAmI.HPC_CLUSTER
    return WhereAmI.DESKTOP


def get_based_on_env(lu: dict):
    # Allow for different values on different systems - convert the keys into WhereAmI enums for lookup
    if not isinstance(lu, dict):
        return lu

    def keyify(k):
        return k if isinstance(k, WhereAmI) else where_am_i_running(k)

    lu = {keyify(k): v for k, v in lu.items()}
    return lu[where_am_i_running()]


def get_data_root():
    where_am_i = where_am_i_running()
    if where_am_i == WhereAmI.CROSSOVER_CLUSTER:
        return Path("/lcrc/project/POLARIS/crossover")
    if where_am_i == WhereAmI.BEBOP_CLUSTER:
        return Path("/lcrc/project/POLARIS/bebop")
    return Path(os.path.expanduser("~/"))
