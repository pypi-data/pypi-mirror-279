import logging
import os
from typing import Optional
import warnings
from copy import deepcopy
from os import PathLike
from pathlib import Path

from polaris.gui.gui import GUI
from polaris.project.project_from_git import clone_and_build
from polaris.runs.convergence.convergence_config import ConvergenceConfig, default_config_filename
from polaris.runs.convergence.convergence_runner import run_polaris_convergence
from polaris.runs.run_utils import get_latest_polaris_output
from polaris.utils.database.migration_manager import DatabaseType, MigrationManager
from polaris.utils.logging_utils import add_file_handler
from polaris.utils.optional_deps import check_dependency


class Polaris:
    """Python interface for all things Polaris

    Running polaris models with this interface is trivial

    ::
        model = Polaris().from_dir("D:/src/argonne/MODELS/bloomington")
        model.run()

    """

    def __init__(self, project_folder=None, scenario_file=None):
        self.__project_folder: Path
        self.__convergence_control = scenario_file or default_config_filename
        self.__database_name = ""
        self.__network = None
        self.__analyze = None
        self.__batch_router = None
        self.run_config: ConvergenceConfig

        if project_folder is not None:
            self.open(project_folder, self.__convergence_control)

    @classmethod
    def from_dir(cls, project_folder, config_file=None):
        config_file = config_file or default_config_filename
        project = Polaris()

        project.open(project_folder, config_file)
        return project

    @classmethod
    def build_from_git(cls, model_dir, city, db_name=None, overwrite=False, inplace=False, branch="main"):
        """Clones a polaris project from git and builds it into a runnable model

        ::

            from polaris import Polaris
            Polaris.from_dir(Polaris.build_from_git("e:/models/from_git", "atlanta"))
        """
        return cls(clone_and_build(model_dir, city, db_name, overwrite, inplace, branch))

    def open(self, model_path: PathLike, config_file: str = default_config_filename) -> None:
        """Opens a Polaris model in memory.  When  a config file is provided, the model tries to load it

        :param model_path: Complete path for the folder containing the Polaris model.
        :param config_file: `Optional`, Name of the convergence control yaml we want to work with. Defaults to *convergence_control.yaml*

        ::

            from polaris import Polaris

            model = Polaris()
            model.open('path/to/model', 'convergence_control_modified.yaml')
        """
        self.__project_folder = Path(model_path)
        self.load_config(Path(config_file))
        logger = logging.getLogger("polaris")
        add_file_handler(logger, logging.WARNING, Path(model_path))

    @property
    def model_path(self) -> Path:
        """Path to the loaded project"""
        return Path(self.__project_folder)

    @property
    def supply_file(self) -> Path:
        """Path to the supply file project"""
        return Path(self.__project_folder) / f"{self.__database_name}-Supply.sqlite"

    @property
    def demand_file(self) -> Path:
        """Path to the supply file project"""
        return self.run_config.data_dir / f"{self.__database_name}-Demand.sqlite"

    @property
    def result_file(self) -> Path:
        """Path to the supply file project"""
        return self.run_config.data_dir / f"{self.__database_name}-Result.sqlite"

    @property
    def network(self):
        for dep in ["geopandas", "aequilibrae", "networkx"]:
            check_dependency(dep, raise_error=True)
        from polaris.network.network import Network

        if self.__network is None:
            self.__network = Network.from_file(self.supply_file)
        return self.__network

    @property
    def analyze(self):
        from polaris.analyze.analyze import Analyze

        self.__analyze = self.__analyze or Analyze(self.supply_file, self.demand_file, self.result_file)
        return self.__analyze

    @property
    def latest_output_dir(self) -> Path:
        return get_latest_polaris_output(self.__project_folder, self.__database_name)

    @property
    def router(self):
        from polaris.runs.router import BatchRouter

        if self.__batch_router is None:
            self.__batch_router = BatchRouter(self.run_config, self.supply_file)
        else:
            warnings.warn("Using router cached in memory")
        return self.__batch_router

    @property
    def gui(self) -> GUI:
        return GUI(self)

    @property
    def skims(self):
        from polaris.skims.skims import Skims

        hwy_name = self.run_config.highway_skim_file_name
        pt_name = self.run_config.transit_skim_file_name
        iter_dir = self.run_config.data_dir
        hwy = iter_dir if os.path.exists(iter_dir / hwy_name) else self.model_path
        pt = iter_dir if os.path.exists(iter_dir / pt_name) else self.model_path
        return Skims(hwy / hwy_name, pt / pt_name)

    def upgrade(self, max_migration: Optional[str] = None):
        """Upgrade the underlying databases to the latest / greatest schema version.

        :param max_migration: a string (date) defining the latest migration id that should be applied. Useful if
                              working with an older version of the POLARIS executable which isn't compatible with
                              the latest schema.

        ::
         model.upgrade("202402")  # only apply upgrades (migrations) from before February 2024.
        """

        DBType = DatabaseType
        MigrationManager.upgrade(self.demand_file, DBType.Demand, redo_triggers=False, max_migration=max_migration)
        MigrationManager.upgrade(self.supply_file, DBType.Supply, redo_triggers=True, max_migration=max_migration)

    def run(self, **kwargs) -> None:
        # Move keywords args that the ConvergenceConfig class knows how to handle into a temp config for this run
        config = deepcopy(self.run_config)
        for k in [k for k in kwargs.keys() if k in config.model_fields]:
            config.__dict__[k] = kwargs[k]
            del kwargs[k]

        # all remaining keyword args passed directly to the run method
        run_polaris_convergence(config, **kwargs)

    def close(self):
        """Eliminates all data from memory

        ::
         model.close()
        """
        del self.__project_folder
        del self.__batch_router
        self.__database_name = ""
        self.__close_all()

    def __close_all(self):
        self.__database_name = ""
        self.__batch_router = None

    def load_config(self, yaml_path: PathLike) -> None:
        """
        :param yaml_path: Name of the YAML file with the full model run configuration

        ::

            model.load_config('my_new_config.json')
        """

        # We can either provide the path to the file or just the json name
        fl = yaml_path if os.path.isfile(yaml_path) else self.__project_folder / yaml_path
        if not os.path.isfile(fl):
            raise FileNotFoundError(f"{fl} not found")

        self.run_config = ConvergenceConfig.from_file(Path(fl))
        self.__database_name = self.run_config.db_name
