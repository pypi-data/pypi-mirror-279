import dataclasses
import datetime
import logging
import re
from pathlib import Path

from polaris.runs.run_utils import seconds_to_str
from polaris.utils.cmd_runner import run_cmd


@dataclasses.dataclass
class PolarisVersion:
    exe_path: Path
    build_date: str
    git_branch: str
    git_sha: str

    @classmethod
    def from_exe(cls, polaris_exe):
        polaris_exe = Path(polaris_exe)
        if polaris_exe.exists():
            output = []
            exit_code = run_cmd(
                f"{polaris_exe} --version", working_dir=polaris_exe.parent, printer=output.append, ignore_errors=True
            )
            if exit_code != 0:
                logging.info(output)
                raise RuntimeError(f"Can't run {polaris_exe} to determine version")
            branch, sha, build_date = parse_polaris_version("\n".join(output))
            return cls(polaris_exe, build_date, branch, sha)
        else:
            return cls(polaris_exe, None, None, None)

    def log(self):
        logging.info(f"    path: {self.exe_path}")
        if self.exe_path.exists():
            logging.info("  exists: ✔")

            if self.build_date is not None:
                delta = seconds_to_str((datetime.datetime.utcnow() - self.build_date).total_seconds())
                build_date_str = f"{self.build_date.strftime('%Y/%m/%d %H:%M:%S')} ({delta} ago)"
            else:
                build_date_str = "Couldn't determine build time"

            logging.info(f"   built: {build_date_str}")
            logging.info(f"  branch: {self.git_branch}")
            logging.info(f"     SHA: {self.git_sha}")
            logging.info(f"     url: https://git-out.gss.anl.gov/polaris/code/polaris-linux/-/commit/{self.git_sha}")

        else:
            logging.info("  exists: ✘")


def parse_polaris_version(exe_output):
    branch, sha, build_date = None, None, None
    m = re.search("Built with git branch: (.*)", exe_output)
    if m is not None:
        branch = m[1].strip()
    m = re.search("Git commit hash: (.*)", exe_output)
    if m is not None:
        sha = m[1].strip()

    m = re.search(r"Compiled at:* (.*) \(UTC\)", exe_output)
    m2 = re.search("This source file was compiled on date (.*) and at the time (.*)", exe_output)
    if m is not None:
        build_date = datetime.datetime.strptime(m[1].strip(), "%Y%m%d-%H%M%S")
    elif m2 is not None:
        a = m2[1].strip()
        b = m2[2].strip()
        build_date = datetime.datetime.strptime(f"{a}-{b}", "%b %d %Y-%H:%M:%S")

    return branch, sha, build_date
