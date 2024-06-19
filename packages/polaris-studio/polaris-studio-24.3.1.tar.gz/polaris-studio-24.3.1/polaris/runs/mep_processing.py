import json
import os
import shutil
import sys
import zipfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import boto3

import pandas as pd

polaris_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(polaris_dir))

from polaris.utils.func_utils import can_fail
from polaris.utils.database.db_utils import read_and_close, run_sql_file, table_to_csv
from polaris.utils.logging_utils import function_logging
from polaris.runs.polaris_inputs import PolarisInputs
from polaris.utils.dir_utils import mkdir_p
from polaris.network.network import Network

sql_dir = Path(__file__).resolve().parent / "sql"
if not sql_dir.exists():
    raise RuntimeError("Something went wrong, SQL directory not found")
mep_dir = Path(__file__).resolve().parent / "mep_files"
if not mep_dir.exists():
    raise RuntimeError("Something went wrong, MEP directory not found")


@dataclass
class MEP_Processor:
    session: boto3.Session = None
    awsS3: boto3.client = None
    awsLambda: boto3.client = None

    @can_fail
    def do_mep(self, sql_dir: Path, results_dir: Path, output_files: PolarisInputs):
        self.create_mep_inputs(sql_dir, results_dir, output_files)
        self.access_aws()
        self.upload_to_mep(sql_dir, results_dir, output_files)
        self.create_payload()
        self.start_job()

    @function_logging("    Creating MEP inputs")
    @can_fail
    def create_mep_inputs(self, results_dir: Path, output_files: PolarisInputs):
        mep_output_dir = results_dir / "mep_inputs"
        mkdir_p(mep_output_dir)
        with read_and_close(output_files.demand_db, spatial=True) as conn:
            run_sql_file(
                sql_dir / "create_MEP_inputs.sql",
                conn,
                attach={"supply": output_files.supply_db, "result": output_files.result_db},
            )
            run_sql_file(sql_dir / "calculate_VOT_adjusted_travel_times_no_adjustment.sql", conn)
            table_to_csv(conn, "link_MEP_calculations", mep_output_dir / "network_results.csv")
            table_to_csv(conn, "activity_by_zone", mep_output_dir / "activities.csv")
            table_to_csv(conn, "zone_parking", mep_output_dir / "park_times.csv")
            table_to_csv(conn, "tnc_wait_times", mep_output_dir / "tnc_wait_times.csv")
            table_to_csv(conn, "model_zones", mep_output_dir / "model_zones.csv")
            table_to_csv(conn, "blocks_mep", mep_output_dir / "blocks.csv")
            table_to_csv(conn, "households_mep", mep_output_dir / "households.csv")
            table_to_csv(conn, "jobs_mep", mep_output_dir / "jobs.csv")
        self.get_e_c_weights(mep_output_dir)
        self.simplify_industries(mep_output_dir / "jobs.csv")
        self.create_gtfs(mep_output_dir, output_files)

    @function_logging("     Get Energy/Cost Weights")
    def get_e_c_weights(self, mep_input_dir: Path):
        # Grab these from default area
        shutil.copyfile("/mnt/r/04 - model results/e_c_weights.csv", mep_input_dir / "e_c_weights.csv")

    @function_logging("     Creating GTFS Input...")
    def create_gtfs(self, results_dir: Path, output_files: PolarisInputs):
        gtfs_dir = results_dir / "gtfs"
        mkdir_p(gtfs_dir)
        my_network = Network()
        my_network.open(str(output_files.supply_db))
        transit = my_network.transit
        transit.export_gtfs(gtfs_dir)
        with zipfile.ZipFile(gtfs_dir / "polaris_gtfs.zip", "r") as zip_ref:
            zip_ref.extractall(gtfs_dir)
        os.remove(gtfs_dir / "polaris_gtfs.zip")

    @function_logging("     Modifying Jobs table with simplified industries")
    def simplify_industries(self, jobs_csv: Path):
        df = pd.read_csv(jobs_csv)
        for index, row in df.iterrows():
            id = int(df.at[index, "sector_id"])
            if id <= 770 or (id >= 6070 and id <= 6390):
                df.at[index, "sector_id"] = "INDUSTRIAL"
                row.sector_id = "INDUSTRIAL"
            elif id <= 3990:
                df.at[index, "sector_id"] = "MANUFACTURING"
            elif id <= 5790:
                df.at[index, "sector_id"] = "RETAIL"
            elif id <= 7790 or (id >= 8660 and id <= 9290):
                df.at[index, "sector_id"] = "SERVICE"
            elif (id >= 7860 and id <= 7890) or (id >= 9370 and id <= 9870):
                df.at[index, "sector_id"] = "GOVERNMENT"
            else:
                df.at[index, "sector_id"] = "OTHER"
        df = df.groupby(["block_id", "sector_id"]).aggregate({"job_count": "sum"})
        df.to_csv(jobs_csv)

    @function_logging("     Accessing MEP AWS account...")
    def access_aws(self):
        aws_profile = None  # Info should be saved on a file in polaris...
        self.session = boto3.Session(profile_name=aws_profile, region_name="us-west-2")
        self.awsS3 = self.session.client("s3")
        self.awsLambda = self.session.client("lambda")

    @function_logging("     Uploading data to MEP Bucket")
    def upload_to_mep(self, input_dir: Path, aws_dir: str):
        for dir, _, files in os.walk(input_dir):
            key = aws_dir
            if "gtfs" in dir:
                key = aws_dir + "/gtfs"
            for f in files:
                self._upload_file_to_mep(Path(dir), f, key)

    def _upload_file_to_mep(self, input_dir: Path, file: str, aws_dir: str):
        print(f"Trying to upload {file}")
        response = self.awsS3.put_object(
            Body=open(input_dir / file, "rb"), Bucket="nrel-mep-shared", Key=f"{aws_dir}/{file}"
        )
        print(response)

    @function_logging("     Uploading data to MEP Bucket")
    def test_get_from_mep(self):
        response = self.awsS3.download_file(
            Bucket="nrel-mep-shared",
            Key="input/polaris/gpra/chicago/s0/e_c_weights.csv",
            Filename="/tmp/e_c_weights.csv",
        )
        print(response)

    @function_logging("     Create Payload from sample json")
    def create_payload(self, scenario: str, aws_key: str, srid: int):
        with open(mep_dir / "payload_template.json", "r") as json_file:
            payload = json.load(json_file)
        # User
        user = payload["user"]
        user["scenarioName"] = scenario
        user["batchName"] = "gpra22"
        user["date"] = date.today().strftime("%Y-%m-%d")
        # Input
        payload_str = json.dumps(payload)
        payload_str = payload_str.replace("EMPTY-SRID", str(srid))
        payload_str = payload_str.replace("EMPTY-KEY", aws_key)
        return payload_str

    @function_logging("     Send Payload for Job Request")
    def start_job(self, payload: str):
        # send the request to invoke the lambda
        response = self.awsLambda.invoke(
            FunctionName="mep-run", InvocationType="RequestResponse", LogType="Tail", Payload=payload
        )
        # read the response
        res_bytes = response["Payload"].read()
        res_json = json.loads(res_bytes.decode("utf-8"))
        print(json.dumps(res_json, sort_keys=True, indent=4))
