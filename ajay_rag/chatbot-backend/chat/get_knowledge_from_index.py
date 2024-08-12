from azure.search.documents import SearchClient
import json
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
from text_embedder.text_embed import TextEmbedder

text_embedder = TextEmbedder()

# Function to retrieve relevant documents based on a query
def get_relevant_documents(query: str):

    # Load configuration from a JSON file
    with open('config.json', 'r') as file:
        config = json.load(file)

    # Initialize Azure Search client
    search_client = SearchClient(
        endpoint=config["SEARCH_ENDPOINT"],
        index_name=config["SEARCH_INDEX_NAME"],
        credential=AzureKeyCredential(config["SEARCH_ADMIN_KEY"])
    )

    # Create a vectorized query using the embedded content
    vector_query = VectorizedQuery(
        vector=text_embedder.embed_content(query), 
        k_nearest_neighbors=3, 
        fields="contentVector"
    )

    # Perform the search with vector queries and select content
    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        select=['content'],
    )

    # Collect the search results into a list
    documents = []
    for result in results:
        documents.append(result)

    return documents  # Return the list of relevant documents
