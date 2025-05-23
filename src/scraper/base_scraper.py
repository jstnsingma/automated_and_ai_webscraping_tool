from src.processor.database_processor import deduplicate_data
from abc import ABC, abstractmethod
import logging
import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    def __init__(self, context):
        self.log = context.log

    @abstractmethod
    async def fetch_html(self)-> str:
        """Fetch HTML content from the URL"""
        pass

    @abstractmethod
    def get_article_list(self, content) -> list[dict]:
        """Return a list of articles metadata"""
        pass

    @abstractmethod
    async def process_all_article(self, content) -> list[dict]:
        """Return a list of articles metadata"""
        pass
    
    async def extract_and_process(self, url) -> list[dict]:
        """Process the article"""

        try:
            async with aiohttp.ClientSession() as session:
                html_content = await self.fetch_html(url, session)

                if html_content:
                    articles = await self.get_article_list(html_content)
                    self.log.info(f"articles: {articles}")
                    
                    dedupe_article = await deduplicate_data(articles)
                    self.log.info(f"deduplicating: {dedupe_article}")

                    all_data = await self.process_all_article(dedupe_article, session)
                    self.log.info(f"all_data: {all_data}")

                    return all_data
        
        except Exception as e:
            self.log.error(f"Error processing article content: {e}")
            raise
