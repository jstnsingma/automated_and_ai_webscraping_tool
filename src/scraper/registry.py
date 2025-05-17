from src.scraper.bbc_scraper import BBCScraper
from src.scraper.npr_scraper import NPRScraper

SCRAPER_REGISTRY = {
    "bbc": {
        "name": "bbc",
        "scraper": BBCScraper,
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml"
    },
    "npr": {
        "name": "NPR",
        "scraper": NPRScraper,
        "url": "https://www.npr.org/get/1001/render/partial/next?start=1&count=50"
    }
}