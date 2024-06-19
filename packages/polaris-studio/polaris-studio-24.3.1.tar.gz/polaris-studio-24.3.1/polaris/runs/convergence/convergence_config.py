import json
import logging
import multiprocessing as mp
import uuid
from pathlib import Path
from typing import Any, Optional, Union, List

import psutil
from polaris.runs.calibrate.calibration_config import CalibrationConfig
from polaris.runs.convergence.convergence_iteration import ConvergenceIteration
from polaris.runs.polaris_version import PolarisVersion
from polaris.utils.config_utils import from_file
from polaris.utils.dir_utils import mkdir_p, with_dir
from polaris.utils.env_utils import is_windows
from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

default_config_filename = "convergence_control.yaml"


class ConvergenceConfig(BaseModel):
    # The following is here to avoid problems in the Cython compiled version of polaris.
    # When compiled, methods (including methods of this class) are no longer "function"s they become "cyfunctions".
    # We use type(mkdir_p) to get that type at runtime so that pydantic doesn't try to check the methods are annotated.
    model_config = ConfigDict(ignored_types=(type(mkdir_p),))

    uuid: str = None
    data_dir: Path = Path(".")
    backup_dir: Path = None
    archive_dir: Path = Path("archive")
    results_dir: Path = Field(default=None, validate_default=True)

    db_name: str = None
    polaris_exe: Optional[Path] = Field(default=None, validate_default=True)
    scenario_skim_file: Path = "scenario_abm.json"
    scenario_main_init: Path = "scenario_abm.json"
    scenario_main: Path = Field(default="scenario_abm.json", validate_default=True)
    async_inline: bool = False
    num_threads: int = mp.cpu_count()
    async_inline: bool = False
    num_abm_runs: int = 2
    num_dta_runs: int = 0
    num_outer_loops: int = 1
    num_workplace_runs: int = 0
    start_iteration_from: Optional[Union[int, str]] = None
    num_retries: int = 1

    do_skim: bool = Field(default=False, validate_default=True)
    do_abm_init: bool = False
    do_pop_synth: bool = Field(default=False, validate_default=True)
    fixed_demand: bool = False

    calibration: CalibrationConfig = CalibrationConfig(enabled=False)
    do_routing_MSA: bool = False

    realtime_informed_vehicle_market_share: Optional[float] = None
    skim_averaging_factor: Optional[float] = None

    capacity_expressway: Optional[float] = None
    capacity_arterial: Optional[float] = None
    capacity_local: Optional[float] = None

    population_scale_factor: float = 1.0
    trajectory_sampling: float = 0.01

    add_rsus: bool = False
    rsu_highway_pr: float = 0.0
    rsu_major_pr: float = 0.0
    rsu_minor_pr: float = 0.0
    rsu_local_pr: float = 0.0
    rsu_enabled_switching: bool = False

    fixed_connectivity_penetration_rates_for_cv: Optional[float] = None

    highway_skim_file_name: str = "highway_skim_file.omx"
    transit_skim_file_name: str = "transit_skim_file.omx"

    skim_interval_endpoints: List[int] = [240, 360, 420, 480, 540, 600, 720, 840, 900, 960, 1020, 1080, 1140, 1200] + [
        1320,
        1440,
    ]

    # This is used to carry around user defined data that needs to be accessible inside callback methods
    user_data: Optional[Any] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.uuid is None:
            self.uuid = uuid.uuid4().hex

    @classmethod
    def from_file(cls, file: Union[str, Path]):
        file_dir = Path(file).parent.resolve()
        return from_file(cls, file).normalise_paths(file_dir)

    @classmethod
    def from_dir(cls, dir: Union[str, Path]):
        config_in_this_dir = Path(dir) / default_config_filename
        config_in_parent_dir = Path(dir).parent / default_config_filename
        if config_in_this_dir.exists():
            return cls.from_file(config_in_this_dir)
        if config_in_parent_dir.exists():
            return cls.from_file(config_in_parent_dir)
        raise FileNotFoundError(f"Can't find {default_config_filename} in {dir} or its parent dir")

    def pretty_print(self, indent=""):
        max_key = max(len(str(k)) for k in self.model_dump().keys())
        return [f"{indent}{k.ljust(max_key)} = {v}" for k, v in self.model_dump().items()]

    def normalise_paths(self, relative_to):
        # print(self)
        with with_dir(relative_to):
            self.data_dir = self.data_dir.resolve()
        with with_dir(self.data_dir):
            self.backup_dir = self.backup_dir.resolve() if self.backup_dir is not None else None
            self.archive_dir = self.archive_dir.resolve()
            self.results_dir = self.results_dir.resolve()
            self.calibration.normalise_paths()

        # If we have less than 200GB lets do our async processing in-line to avoid memory issues
        if (psutil.virtual_memory().total < 200000000000) and self.db_name in ["Chicago", "Detroit", "Atlanta"]:
            self.async_inline = True

        if self.db_name is None:
            with open(self.data_dir / self.scenario_main, "r") as fl:
                scenario_config = json.load(fl)
            self.db_name = scenario_config["General simulation controls"]["database_name"]

        return self

    def supply_file(self):
        return Path(f"{self.db_name}-Supply.sqlite")

    def demand_file(self):
        return Path(f"{self.db_name}-Demand.sqlite")

    def result_file(self):
        return Path(f"{self.db_name}-Result.sqlite")

    def iterations(self):
        setup_iterations = []
        if self.do_skim:
            setup_iterations.append(ConvergenceIteration(is_skim=True))
        if self.do_pop_synth:
            setup_iterations.append(ConvergenceIteration(is_pop_synth=True))
        if self.do_abm_init:
            setup_iterations.append(ConvergenceIteration(is_abm_init=True))

        iterations = []
        for _ in range(1, self.num_outer_loops + 1):
            iterations += [
                ConvergenceIteration(fixed_demand=self.fixed_demand) for _ in range(1, self.num_abm_runs + 1)
            ]
            iterations += [ConvergenceIteration(is_dta=True) for _ in range(1, self.num_dta_runs + 1)]
        for i, it in enumerate(iterations):
            it.iteration_number = i + 1
        if iterations != []:
            iterations[-1].is_last = True

        self.num_workplace_runs = min(self.num_workplace_runs, len(iterations))
        return self.filter_based_on_start_iter(setup_iterations + iterations, self.start_iteration_from)

    def filter_based_on_start_iter(self, iterations, start_from=None):
        start_from = start_from or self.start_iteration_from

        if not start_from:
            return iterations

        # if it's an integer - create a string reprr of the corresponding normal iteration object
        if isinstance(start_from, int) or start_from.isdigit():
            start_from = str(ConvergenceIteration.of_type("normal", start_from))

        try:
            idx = [str(e) for e in iterations].index(str(start_from))
            return iterations[idx:]
        except:
            doing_str = ",".join([str(e) for e in iterations])
            raise RuntimeError(f"Couldn't start from {start_from}, it's not in the list we are doing {doing_str}")

    def check_exe(self):
        logging.info("POLARIS Executable:")
        ver = PolarisVersion.from_exe(self.polaris_exe)
        ver.log()

    # -------------------------------------------------------------------------------
    # Validators for populating default values (can be based on other defined values)
    # -------------------------------------------------------------------------------
    @field_validator("results_dir", mode="before")
    # def default_results_dir(cls, v, *, values, **kwargs):
    def val_results_dir(cls, v, info: ValidationInfo) -> Path:
        return v or (info.data["data_dir"] / "simulation_results")

    @field_validator("polaris_exe", mode="before")
    def default_polaris_exe(cls, v, info: ValidationInfo):
        exists = lambda x: Path(x).absolute() if x and Path(x).exists() else None
        extension = ".exe" if is_windows() else ""
        model_bin = info.data["data_dir"] / "bin" / f"Integrated_Model{extension}"
        polaris_bin = Path(__file__).parent.parent.parent / "bin" / f"Integrated_Model{extension}"
        return exists(v) or exists(model_bin) or exists(polaris_bin)

    @field_validator("scenario_main", mode="before")
    def default_scenario_main(cls, v, info: ValidationInfo):
        return v or (info.data["data_dir"] / "scenario_abm.json")

    @field_validator("do_pop_synth", mode="before")
    def default_do_pop_synth(cls, v, info: ValidationInfo):
        return not not v

    @field_validator("do_skim", mode="before")
    def default_do_skim(cls, v, info: ValidationInfo):
        return v and "scenario_skim_file" in info.data

    # -------------------------------------------------------------------------------
