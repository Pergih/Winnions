from dagster import Definitions

from winnions.jobs.run_extract import run_extract_job
from winnions.schedules.extract_schedule import extract_schedule

defs = Definitions(
    jobs=[run_extract_job],
    schedules=[extract_schedule],
)
