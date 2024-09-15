import os
import pandas as pd
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

import minsearch


load_dotenv()

USE_ELASTIC = os.getenv("USE_ELASTIC")
ELASTIC_URL = os.getenv("ELASTIC_URL") # ELASTIC_URL_LOCAL
INDEX_MODEL_NAME = os.getenv("INDEX_MODEL_NAME", "multi-qa-MiniLM-L6-cos-v1")
INDEX_NAME = os.getenv("INDEX_NAME")
DATA_PATH = os.getenv("DATA_PATH", "data/Azure-DP-900.apkg.csv")
BASE_URL = "https://github.com/dmytrovoytko/llm-exam-assistant/blob/main"

def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)

    documents = df.to_dict(orient="records")

    index = minsearch.Index(
        text_fields=[
            "question",
            "answer",
            "exam",
            "section",
        ],
        keyword_fields=["id"],
    )

    index.fit(documents)
    return index


def fetch_documents():
    print("Fetching documents...")
    relative_url = "data/Azure-DP-900.apkg.csv"
    docs_url = relative_url # f"{BASE_URL}/{relative_url}?raw=1"
    # docs_response = requests.get(docs_url)
    # documents = docs_response.json()
    df = pd.read_csv(docs_url)
    documents = df.to_dict(orient="records")
    print(f"Fetched {len(documents)} documents")
    return documents


def setup_elasticsearch():
    print(f"Setting up Elasticsearch ({ELASTIC_URL})...")
    es_client = Elasticsearch(ELASTIC_URL)
    print(" Connected to Elasticsearch:", es_client.info())

    index_settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "question": {"type": "text"},
                "answer": {"type": "text"},
                "exam": {"type": "keyword"},
                "section": {"type": "text"},
                "id": {"type": "keyword"},
                "question_text_vector": {
                    "type": "dense_vector",
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine",
                },
            }
        },
    }

    try:
        es_client.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    except Exception as e:
        print('!! es_client.indices.delete:', e)
    es_client.indices.create(index=INDEX_NAME, body=index_settings)
    print(f"Elasticsearch index '{INDEX_NAME}' created")
    return es_client


def load_model():
    print(f"Loading model: {INDEX_MODEL_NAME}")
    return SentenceTransformer(INDEX_MODEL_NAME)


def index_documents(es_client, documents, model):
    print("Indexing documents...")
    for doc in documents:
        question = doc["question"]
        text = doc["answer"]
        doc["question_text_vector"] = model.encode(question + " " + text).tolist()
        es_client.index(index=INDEX_NAME, document=doc)
    print(f" Indexed {len(documents)} documents")


def init_elasticsearch():
    # you may consider to comment <start>
    # if you just want to init the db or didn't want to re-index
    print("Starting the indexing process...")

    documents = fetch_documents()
    # ground_truth = fetch_ground_truth()
    model = load_model()
    es_client = setup_elasticsearch()
    index_documents(es_client, documents, model)
    # you may consider to comment <end>

    # print("Initializing database...")
    # init_db()

    print("Indexing process completed successfully!")


if __name__ == "__main__":
    if USE_ELASTIC:
        init_elasticsearch()
    else:
        print("MinSearch: Ingesting data...")
        index = load_index(data_path=DATA_PATH)
        print(f' Indexed {len(index.docs)} document(s)')