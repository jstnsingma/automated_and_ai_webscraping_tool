from pinecone.grpc import PineconeGRPC as Pinecone
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()

class PineconeHelper:
    def __init__(self):
        self.api_key = os.getenv("PC_API_KEY")
        self.host = os.getenv("PC_HOST")
        self.pc = Pinecone(api_key=self.api_key)
        self.index = self.pc.Index(host=self.host)

    def upsert_vectors(self, vectors: List[Dict]):
        return self.index.upsert(vectors=vectors)
    
    def fetch_vectors(self, id: List):
        results = self.index.fetch(ids=id)
        return results.vectors
