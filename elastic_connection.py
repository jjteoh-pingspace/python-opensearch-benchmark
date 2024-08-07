from opensearchpy import OpenSearch
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()


# Get OpenSearch configuration from environment variables
# OPENSEARCH_URL = os.getenv('OPENSEARCH_URL')
OPENSEARCH_HOST = os.getenv('OPENSEARCH_HOST')
OPENSEARCH_PORT = os.getenv('OPENSEARCH_PORT')
OPENSEARCH_USER = os.getenv('OPENSEARCH_USER')
OPENSEARCH_PASSWORD = os.getenv('OPENSEARCH_PASSWORD')


def get_es_connection(retries=5, delay=3):
    for attempt in range(retries):
        try:
            print("hello")
            es = OpenSearch(
                # [OPENSEARCH_URL],
                hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT, }],
                http_auth=(OPENSEARCH_USER, OPENSEARCH_PASSWORD),
                ssl_show_warn=False,
                verify_certs=False,
                use_ssl=True,
                # connection_class=RequestsHttpConnection
            )
            return es
        except Exception as e:
            print("Failed to connect OpenSearch", e)
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print.error(
                    "Failed to connect to OpenSearch after several attempts.")
                raise e


es = get_es_connection()

print(OPENSEARCH_HOST)
print(OPENSEARCH_PORT)
print(OPENSEARCH_USER)
print(OPENSEARCH_PASSWORD)
