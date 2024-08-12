from azure.search.documents import SearchIndexingBufferedSender
import json
from azure.core.credentials import AzureKeyCredential
from typing import List
import logging
import uuid

# Function to index documents into Azure Search
def index_documents(docs: List[dict]):

    # Load configuration from JSON file
    with open('config.json', 'r') as file:
        config = json.load(file)
    
    items = []
    for item in docs:
        unique_id = uuid.uuid4()  # Generate a unique ID for each document
        logging.info(f"the unique id is :{unique_id}")
        items.append({
            "id": str(unique_id),
            "content": item["pageContent"],
            "contentVector": item["embedding"],
            "pageNumber": str(item["pageNumber"]),
        })
    
    try:
        # Initialize batch client and upload documents
        with SearchIndexingBufferedSender(
            endpoint=config["SEARCH_ENDPOINT"],
            index_name=config["SEARCH_INDEX_NAME"],
            credential=AzureKeyCredential(config["SEARCH_ADMIN_KEY"])
        ) as batch_client:
            logging.info(f"the items[0] is {items[0]}")
            batch_client.upload_documents(documents=items)
    except Exception as e:
        logging.info(f"the error is {e}")
    
    return "the documents uploaded"  # Confirm successful upload
