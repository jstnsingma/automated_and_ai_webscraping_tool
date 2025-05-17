from src.scraper.base_scraper import BaseScraper
from bs4 import BeautifulSoup
from datetime import datetime
from src.utils.utils import custom_serializer
import logging
import aiohttp
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BBCScraper(BaseScraper):

    async def fetch_html(self, url: str, session: aiohttp.ClientSession) -> str:
        """Fetch HTML content from the URL"""

        try: 
            headers = {"User-Agent": "Mozilla/5.0"}
            logger.info(f"Fetching HTML content from {url}")
            async with session.get(url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()
                logger.info(f"Successfully fetched: {url}")

                return html_content

        except Exception as e:
            logger.exception(f"Unexpected error on {url}: {e}")
            raise

    async def get_article_list(self, content: str) -> list[dict]:
        """Fetch a list of articles metadata"""

        try:
            soup = BeautifulSoup(content, "xml")
            articles  = []
            items = soup.find_all("item")

            for item in items:
                title = item.title.text
                link = item.link.text
                pub_date = item.pubDate.text

                pub_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
                pub_date = custom_serializer(pub_date)

                # Cleans the title
                cleaned_title = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', title)

                articles.append({
                    "title": cleaned_title,
                    "url": link,
                    "date": pub_date
                })

            return articles 
        
        except Exception as e:
            logger.exception(f"Error parsing article list: {e}")
            raise
    
    async def process_all_article(self, articles: list[dict], session: aiohttp.ClientSession) -> dict:
        """Fetch and process the article from the URL"""
        
        all_data = []

        for article in articles:
            if not re.search(r'/news/videos/', article['url']):
                try:
                    url = article['url']
                    html_content = await self.fetch_html(url, session)
                    soup = BeautifulSoup(html_content, "html.parser")

                    # Title
                    title = article['title']

                    # Date
                    date = article['date']

                    # Authors
                    byline_div = soup.find('div', attrs={'data-testid': 'byline-new-contributors'})
                    author = byline_div.find('span').get_text(strip=True)

                    # Content
                    text_blocks = soup.find_all('div', class_="sc-3b6b161a-0 dEGcKf")
                    p_tags = [p for block in text_blocks for p in block.find_all('p')]
                    full_content = ' '.join(p.get_text(strip=True) for p in p_tags)

                    all_data.append({
                        'title': title,
                        'date': date,
                        'author': author,
                        'source': url,
                        'content': full_content
                        })
            
                except Exception as e:
                    logger.exception(f"Failed to process article at {article['url']}: {e}")
                    continue
        
        with open("rueters_processed.json", "w") as f:
            json.dump(all_data, f, indent=4)
        
        return all_data

    async def main(self, url: str, context):
        return await self.extract_and_process(url, context)