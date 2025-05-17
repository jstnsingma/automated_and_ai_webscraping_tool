from src.helper.pinecone_helper import PineconeHelper
from src.helper.b2_helper import B2Helper
from src.utils.utils import content_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_archiving(article: list[dict]):
    """ Saving json file to b2 bucket """

    bucket_name = "archived-news"
    helper = B2Helper(bucket_name)
    helper.upload_file(article['data'], article['name'])

def save_to_db(article: list[dict]):
    """ Saving to pinecone db """

    pc_helper = PineconeHelper()
    pc_helper.upsert_vectors(article)

async def deduplicate_data(datas: list[dict]) -> list[dict]:
    """ Filters the data that are already in the DB """

    logger.info(f"Processing deduplication")
    pc_helper = PineconeHelper()

    id_data_pairs = [(content_hash(data['url']), data) for data in datas]
    ids = [pair[0] for pair in id_data_pairs]
    result = pc_helper.fetch_vectors(ids)

    existing_ids = [data['id'] for data in result.values()]
    new_data = [data for (hash_id, data) in id_data_pairs if hash_id not in existing_ids]

    return new_data
