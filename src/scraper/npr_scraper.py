from src.scraper.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import logging
import aiohttp

class NPRScraper(BaseScraper):

    def __init__(self, context):
        super().__init__(context)
        self.log = context.log

    async def fetch_html(self, url: str, session: aiohttp.ClientSession) -> str:
        """Fetch HTML content from the URL"""

        try: 
            headers = {"User-Agent": "Mozilla/5.0"}
            async with session.get(url, headers=headers) as response:
                response.raise_for_status() 
                html_content = await response.text()

                return html_content

        except Exception as e:
            self.log.error(f"Unexpected error on {url}: {e}")
            raise

    async def get_article_list(self, content: str):
        """Fetch a list of articles metadata"""

        try:
            soup = BeautifulSoup(content, "html.parser")
            results = []

            for item in soup.select("div.item-info-wrap"):
                title_tag = item.select_one("h2.title a")
                time_tag = item.select_one("p.teaser time")

                if title_tag and time_tag:
                    results.append({
                        "title": title_tag.text.strip(),
                        "url": title_tag['href'],
                        "date": time_tag.get("datetime")
                    })
            
            return results
        
        except Exception as e:
            self.log.error(f"Error parsing article list: {e}")
            raise
    
    async def process_all_article(self, articles: list[dict], session: aiohttp.ClientSession) -> dict:
        """Fetch and scraped the article from the URL"""
        
        all_data = []

        for article in articles:
            try:
                url = article['url']
                html_content = await self.fetch_html(url, session)
                soup = BeautifulSoup(html_content, "html.parser")

                # Title
                h1_tag = soup.find('h1')
                title = h1_tag.get_text(strip=True)

                # Date
                date_tag = soup.find('time')
                date = date_tag.get('datetime')

                # Authors
                author_tags = soup.find_all('p', class_='byline__name byline__name--block')
                authors = [author.get_text(strip=True) for author in author_tags]

                # Content
                credit_caption_div = soup.find('div', class_='storytext storylocation linkLocation')
                p_tags = credit_caption_div.find_all('p')
                full_content = ' '.join(p.get_text(strip=True) for p in p_tags)

                all_data.append({
                    'title': title,
                    'date': date,
                    'author': authors,
                    'source': url,
                    'content': full_content
                    })
        
            except Exception as e:
                self.log.error(f"Failed to process article at {article['url']}: {e}")
                continue

        self.log.info(f"all_data: {all_data}")
        return all_data

    async def main(self, url):
        return await self.extract_and_process(url)