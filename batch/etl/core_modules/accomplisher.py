import boto3
from datetime import datetime, timezone
from etl.core_modules.base.base_processor import BaseProcessor


class Accomplisher(BaseProcessor):
    JOB_NAME = "etl_accomplisher_job"

    def __init__(self, args, data_writer):
        super().__init__(args, self.JOB_NAME, None)
        self.ssm_client = boto3.client("ssm")

        self.parameter_name = self.args.get(
            "ssm_parameter_name", "/batch/last-successful-run"
        )
        self.logger.info(f"SSM Parameter to update: '{self.parameter_name}'")

    def process(self):
        self.logger.info(
            f"Starting accomplishment process for end_date string: '{self.end_date}'"
        )

        if not isinstance(self.end_date, str) or not self.end_date:
            self.logger.error(
                f"Invalid input: 'end_date' is not a valid string. Found: {self.end_date}"
            )
            return False

        try:
            date_format = "%Y-%m-%dT%H"
            completion_timestamp = datetime.strptime(
                self.end_date, date_format
            ).replace(tzinfo=timezone.utc)
            self.logger.info(
                f"Successfully parsed end_date to datetime object: {completion_timestamp}"
            )

        except ValueError:
            self.logger.error(
                f"Date format error: Could not parse '{self.end_date}' with format '{date_format}'."
            )
            return False

        success = self._update_last_successful_run(completion_timestamp)

        if success:
            self.logger.info("Accomplishment process finished successfully.")
        else:
            self.logger.error(
                "Accomplishment process failed. Check previous logs for details."
            )

        return success

    def _update_last_successful_run(self, timestamp_to_set: datetime) -> bool:
        try:
            timestamp_str = timestamp_to_set.isoformat()
            self.logger.info(
                f"Attempting to update SSM Parameter '{self.parameter_name}' with value: {timestamp_str}"
            )

            self.ssm_client.put_parameter(
                Name=self.parameter_name,
                Description="Timestamp of the last successful batch run, set by ETL Accomplisher.",
                Value=timestamp_str,
                Type="String",
                Overwrite=True,
                Tier="Advanced",
            )

            self.logger.info(f"Successfully updated parameter '{self.parameter_name}'.")
            return True
        except Exception as e:
            self.logger.error(
                f"Failed to update SSM parameter '{self.parameter_name}': {e}",
                exc_info=True,
            )
            return False
