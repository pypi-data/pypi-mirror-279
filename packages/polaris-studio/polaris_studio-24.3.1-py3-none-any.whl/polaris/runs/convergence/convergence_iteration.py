import dataclasses
import uuid
from pathlib import Path
from typing import Optional

from polaris.runs.polaris_inputs import PolarisInputs


@dataclasses.dataclass
class ConvergenceIteration:
    uuid: str = None
    is_skim: bool = False
    is_pop_synth: bool = False
    is_abm_init: bool = False
    is_dta: bool = False
    is_last: bool = False
    fixed_demand: bool = False
    iteration_number: int = -1
    runtime: float = 0
    output_dir: Optional[Path] = None
    scenario_file: Optional[Path] = None
    files: Optional[PolarisInputs] = None

    previous_iteration: Optional["ConvergenceIteration"] = None
    next_iteration: Optional["ConvergenceIteration"] = None

    @property
    def is_standard(self):
        return not any([self.is_pop_synth, self.is_abm_init, self.is_skim, self.is_dta])

    @classmethod
    def of_type(cls, iteration_type, iteration_number):
        if iteration_type is None or iteration_type == "normal":
            return ConvergenceIteration(iteration_number=iteration_number)
        if iteration_type == "skim":
            return ConvergenceIteration(is_skim=True, iteration_number=iteration_number)
        elif iteration_type == "abm_init":
            return ConvergenceIteration(is_abm_init=True, iteration_number=iteration_number)
        elif iteration_type == "pop_synth":
            return ConvergenceIteration(is_pop_synth=True, iteration_number=iteration_number)
        elif iteration_type == "dta":
            return ConvergenceIteration(is_dta=True, iteration_number=iteration_number)
        raise RuntimeError(f"Unknown iteration type: {iteration_type}")

    @classmethod
    def from_dir(cls, dir, db_name=None, it_type=None, it_num=None):
        # If they aren't specified we can parse these props from the dirname
        if not db_name or not it_type or not it_num:
            db_name, it_type, it_num = cls.parse_dirname(dir)
        iteration = cls.of_type(it_type, it_num)
        iteration.output_dir = Path(dir)
        iteration.files = PolarisInputs.from_dir(Path(dir), db_name)
        return iteration

    def type(self):
        if self.is_skim:
            return "skim"
        if self.is_pop_synth:
            return "pop_synth"
        if self.is_abm_init:
            return "abm_init"
        if self.is_dta:
            return "dta"
        return "normal (fixed demand)" if self.fixed_demand else "normal"

    def __str__(self):
        if self.is_skim:
            if self.iteration_number >= 0:
                return f"00_skim_iteration_{self.iteration_number}"
            else:
                return "00_skim_iteration"
        if self.is_abm_init:
            return "01_abm_init_iteration"
        if self.is_pop_synth:
            return "02_pop_synth_iteration"
        if self.is_dta:
            return f"dta_iteration_{self.iteration_number}"
        return f"iteration_{self.iteration_number}"

    def __format__(self, *args, **kwargs):
        return str(self).__format__(*args, **kwargs)

    def set_output_dir(self, output_dir: Path, scenario_file: Path, db_name: str):
        """
        This method is called when an iteration has actually been run. It sets the actual paths to the output folder
        and scenario file that was used to run the iteration as well as storing the auto-generated uuid in that folder.
        """
        self.output_dir = output_dir
        self.files = PolarisInputs.from_dir(output_dir, db_name)
        self.scenario_file = output_dir / "model_files" / scenario_file.name
        uuid_file = output_dir / "uuid"
        if uuid_file.exists():
            with open(output_dir / "uuid", "r") as f:
                self.uuid = f.read()
        else:
            self.uuid = uuid.uuid4().hex
            with open(output_dir / "uuid", "w") as f:
                f.write(self.uuid)

    @staticmethod
    def parse_dirname(dirname):
        dirname = Path(dirname).name
        if "abm_init" in dirname:
            return dirname.replace("_01_abm_init_iteration", ""), "abm_init", None
        if "pop_synth" in dirname:
            return dirname.replace("_02_pop_synth_iteration", ""), "pop_synth", None

        if "skim_iteration" in dirname:
            it_type = "skim"
            if dirname.endswith("00_skim_iteration"):
                return dirname.replace("_00_skim_iteration", ""), "skim", None
            db, num = dirname.split("_00_skim_iteration_")
            return db, "skim", int(num)

        db, num = dirname.split("_iteration_")
        return db, "normal", int(num)
