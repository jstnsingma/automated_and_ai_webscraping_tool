import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

class GeminiHelper:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API")
        self.model = "text-embedding-004"
        genai.configure(api_key=self.api_key)

    def embed_data(self, data):
        result = genai.embed_content(model=self.model, content=data)
        return result['embedding']

