from opensearchpy import OpenSearch
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenSearch configuration from environment variables
OPENSEARCH_URL = os.getenv('OPENSEARCH_URL')
OPENSEARCH_USER = os.getenv('OPENSEARCH_USER')
OPENSEARCH_PASSWORD = os.getenv('OPENSEARCH_PASSWORD')

es = OpenSearch(
    [OPENSEARCH_URL],
    http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
    ssl_show_warn=False,
    verify_certs=False
)

try:
    info = es.info()
    print("OpenSearch info:", info)
except Exception as e:
    print("Error connecting to OpenSearch:", e)
