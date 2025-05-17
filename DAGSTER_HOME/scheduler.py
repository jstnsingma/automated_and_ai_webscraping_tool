from dagster import Definitions, ScheduleDefinition
from DAGSTER_HOME.pipeline import run_all_scrapers  

daily_schedule = ScheduleDefinition(
    job=run_all_scrapers,
    cron_schedule="0 0 * * *", 
    name="daily_scraping_schedule"
)

defs = Definitions(
    jobs=[run_all_scrapers],
    schedules=[daily_schedule]
)