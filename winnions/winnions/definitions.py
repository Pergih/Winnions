from dagster import Definitions, load_assets_from_modules

from winnions.jobs.run_extract import run_extract_job
from winnions.schedules.extract_schedule import extract_schedule

from winnions import assets  # noqa: TID252

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    jobs=[run_extract_job],
    schedules=[extract_schedule],
)
