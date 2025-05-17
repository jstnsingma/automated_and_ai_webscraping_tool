from b2sdk.v2 import InMemoryAccountInfo, B2Api
from dotenv import load_dotenv
from datetime import datetime
import json
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

class B2Helper:
    def __init__(self, bucket_name: str):
        info = InMemoryAccountInfo()
        self.b2_api = B2Api(info)
        self.b2_api_id = os.getenv("B2_KEY_ID")
        self.b2_app_key = os.getenv("B2_APP_KEY")
        self.b2_api.authorize_account("production", application_key_id=self.b2_api_id, application_key=self.b2_app_key)
        self.bucket = self.b2_api.get_bucket_by_name(bucket_name)
        self.date_today = datetime.today().strftime("%m-%d-%Y")

    def upload_file(self, data: dict, web_name):
        
        try:
            file_name = f"{web_name}_{self.date_today}.json"
            article_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")

            self.bucket.upload_bytes(
                data_bytes=article_bytes,
                file_name=file_name,
                content_type='application/json'
            )
        except Exception as e:
            logger.error(f"Unexpected error on uploading at {web_name}: {e}")
            raise
