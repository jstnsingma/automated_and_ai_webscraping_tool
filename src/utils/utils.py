import hashlib
from datetime import datetime

def content_hash(url: str) -> str:
    return hashlib.sha256(url.strip().encode('utf-8')).hexdigest()

def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")