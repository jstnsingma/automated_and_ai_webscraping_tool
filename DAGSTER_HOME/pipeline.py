from dagster import op, DynamicOut, DynamicOutput, Out, job, graph
from src.scraper.registry import SCRAPER_REGISTRY
from src.processor.article_processor import start_scraper, process_articles
from src.processor.database_processor import process_archiving, save_to_db

@op(out=DynamicOut())
async def extract_bbc(context):
    context.log.info("Instantiating extract_bbc")
    name = SCRAPER_REGISTRY["bbc"]["name"]
    url = SCRAPER_REGISTRY["bbc"]["url"]
    scraper = SCRAPER_REGISTRY["bbc"]["scraper"]

    result = await start_scraper(scraper, url, name)
    data, name = result    

    context.log.info(f"bbc data: {data}")
    context.log.info("Instantiating extract_npr finished")
    yield DynamicOutput(data, mapping_key=name)

@op(out=DynamicOut())
async def extract_npr(context):
    context.log.info("Instantiating extract_npr")
    name = SCRAPER_REGISTRY["npr"]["name"]
    url = SCRAPER_REGISTRY["npr"]["url"]
    scraper = SCRAPER_REGISTRY["npr"]["scraper"]

    result = await start_scraper(scraper, url, name)
    data, name = result    

    context.log.info(f"npr data: {data}")
    context.log.info("Instantiating extract_npr finished")
    yield DynamicOutput(data, mapping_key=name)

@op(out=Out())
def archive_article(article_data: dict):
    process_archiving(article_data)
    return article_data

@op(out=Out())
def summarize_and_categorize(article_data):
    return process_articles(article_data['data'])

@op
def store_articles(article: list[dict]):
    save_to_db(article)

@graph
def web_scraper():
    extract_bbc().map(archive_article).map(summarize_and_categorize).map(store_articles)

@graph
def web_scraper2():
    extract_npr().map(archive_article).map(summarize_and_categorize).map(store_articles)

@job
def run_all_scrapers():
    web_scraper()
    web_scraper2()
