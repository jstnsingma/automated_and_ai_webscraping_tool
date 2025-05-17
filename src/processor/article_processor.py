from src.helper.llama_helper import LlamaClient
from src.helper.gemini_helper import GeminiHelper
from src.utils.utils import content_hash
import logging
import asyncio
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_scraper(scraper_cls, url, name, context):
    context.log.info(f"calling scraper: {name}")
    logger.info(f"Instantiating scraper: {scraper_cls.__name__}")

    article_dict = {}
    try:
        article_data = await scraper_cls().main(url, context)
        context.log.info(f"{name}: article_data: {article_data}")
        article_dict['data'] = article_data
        article_dict['name'] = name

        await asyncio.sleep(2)
        logger.info(f"Done Instantiating: {scraper_cls.__name__}")

        return article_dict, name
    
    except Exception as e:
        logger.exception(f"Scraper error({scraper_cls.__name__}) failed: {e}")
        return None, name

def process_articles(article_data) -> list[dict]:
    processed_articles = []
    try:
        llama = LlamaClient()
        gemini = GeminiHelper()
        
        # Set to x due to free tier 
        for i in range(2):
            data = {}
            summary = llama.summarize_and_categorize(article_data[i]['content'])

            article_data[i]['content'] = summary['content']
            article_data[i]['category'] = summary['category']
            article_data[i]['importance'] = summary['importance']

            values = gemini.embed_data(f"{article_data[i]['title']}\n\n{article_data[i]['category']}")
            id = content_hash(article_data[i]['source'])
            
            data['id'] = id
            data['values'] = values
            data["metadata"] = article_data[i]

            processed_articles.append(data)

        return processed_articles
    

        # # Uncomment if no longer free tier    
        # for article in article_data:
        #     data = {}
        #     summary = llama.summarize_and_categorize(article['content'])

        #     article['content'] = summary['content']
        #     article['category'] = summary['category']
        #     article['importance'] = summary['importance']

        #     values = gemini.embed_data(f"{article['title']}\n\n{article['content']}")

        #     data['id'] = f"news{i}"
        #     data['values'] = values
        #     data["metadata"] = article_data

        #     processed_articles.append(data)
            
        #     time.sleep(1.5)
        
        # with open ("processed_articles.txt", 'w') as f:
        #     f.write(processed_articles)

        # return processed_articles
    
    except Exception as e:
        logger.exception(f"Error processing articles: {e}")

