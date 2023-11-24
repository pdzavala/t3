import os
from google.api_core.protobuf_helpers import get_messages
from google.cloud import storage
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

GOOGLE_APPLICATION_CREDENTIAL = os.getenv('GOOGLE_APPLICATION_CREDENTIAL')
BUCKET_NAME = os.getenv('BUCKET_NAME')

class Bucket:
    def __init__(self, storage_client):
        self.client = storage_client

    def list_blobs(self, bucket_name):
        blobs = self.client.list_blobs(bucket_name)
        return blobs

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

for blob in Bucket.list_blobs(BUCKET_NAME):
    print(blob.name)