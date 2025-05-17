from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests
from dotenv import load_dotenv
import os
import logging
import json

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LlamaClient:

    def __init__(self):
        self.api_key = os.getenv("LLAMA_API")
        self.url = os.getenv("LLAMA_URL")
        self.base_dir = os.path.dirname(__file__)
    
    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=30, max=30),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def query_llama_3(self, prompt, temperature=0.7):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature
        }

        try:
            response = requests.post(self.url, headers=headers, json=payload)
            response.raise_for_status() 

            return response.json()["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            print(f"Request AI failed: {e}")
            raise
        
    def load_prompt(self, file_path):
        try: 
            with open(file_path, "r") as f:
                return f.read()
            
        except FileNotFoundError as e:
            logger.exception(f"Error reading file not found: {file_path}")
        
    def summarize_and_categorize(self, article):
        try:
            prompt_path = os.path.join(self.base_dir, "prompts", "summarize_and_categorize.txt")
            prompt_template = self.load_prompt(prompt_path)
            prompt = prompt_template.format(article=article)
            result = self.query_llama_3(prompt)

            logger.info(f"LLM RESULT: {result}")

            return json.loads(result)
        
        except (KeyError, RuntimeError) as e:
            logger.exception(f"Failed to summarize and categorize article: {e}")
            raise