from azure.search.documents import SearchIndexingBufferedSender
import json
from azure.core.credentials import AzureKeyCredential
import uuid
from text_embedder.text_embed import TextEmbedder

text_embedder = TextEmbedder()

# Function to upload a conversation into the memory index
def upload_memory_into_index(query: str, answer: str):
    
    # Load configuration from a JSON file
    with open('config.json', 'r') as file:
        config = json.load(file)
    
    unique_id = uuid.uuid4()  # Generate a unique ID for the document
    
    # Format the conversation as a string
    Q_and_A = "user: " + query + "\n" + "Assistant: " + answer
    
    # Create a document with content and its vectorized form
    doc = {
        "id": str(unique_id),
        "content": Q_and_A,
        "contentVector": text_embedder.embed_content(Q_and_A)
    }
    
    # Upload the document to the memory index
    with SearchIndexingBufferedSender(
        endpoint=config["SEARCH_ENDPOINT"],
        index_name=config["MEMORY_INDEX_NAME"],
        credential=AzureKeyCredential(config["SEARCH_ADMIN_KEY"])
    ) as batch_client:
        batch_client.upload_documents(documents=[doc])

    return f"Conversation uploaded to memory index"  # Confirm upload
