from pathlib import Path

from pydantic import BaseModel


class CalibrationConfig(BaseModel):
    enabled: bool = False

    target_csv_dir: Path = "calibration_targets"

    first_calibration_iteration: int = 1
    calibrate_every_x_iter: int = 4

    calibrate_activities: bool = True
    calibrate_destinations: bool = True
    calibrate_modes: bool = True
    calibrate_timings: bool = True

    step_size: float = 2.0

    # hack this in here until we can figure a way to get warm_start_act to not THROW_EXCEPTION
    warm_calibrating: bool = False

    def normalise_paths(self):
        self.target_csv_dir = Path(self.target_csv_dir).resolve()

    def should_calibrate(self, iteration):
        i = iteration.iteration_number - self.first_calibration_iteration
        x = self.calibrate_every_x_iter
        return i % x == 0 and self.enabled and iteration.is_standard
