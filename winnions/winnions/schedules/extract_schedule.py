from dagster import schedule

from winnions.jobs.run_extract import *

@schedule(cron_schedule = "0 10 * * *", job=run_extract_job, execution_timezone="US/Central")
def extract_schedule(_context):
    run_config = {}
    return run_config