from dagster import Definitions, ScheduleDefinition
from DAGSTER_HOME.pipeline import run_all_scrapers, extract_bbc, extract_npr

daily_schedule = ScheduleDefinition(
    job=run_all_scrapers,
    cron_schedule="0 0 * * *", 
    name="daily_scraping_schedule"
)

defs = Definitions(
    assets=[extract_bbc, extract_npr],
    jobs=[run_all_scrapers],
    schedules=[daily_schedule]
)