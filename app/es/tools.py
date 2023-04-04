# from app.es.es import es_client
import elasticsearch
from elasticsearch import Elasticsearch
import time

ES_HOST = 'http://elasticsearch:9200'

index_create_settings = {
  "analysis": {
    "filter": {
      "english_stemmer": {
        "type":       "stemmer",
        "language":   "english"
      },
      "russian_stemmer": {
        "type":       "stemmer",
        "language":   "russian"
      },
    },
    "analyzer": {
      "ru_en": {
        "tokenizer":  "standard",
        "filter": [
          "lowercase",
          "russian_stemmer",
          "english_stemmer"
        ]
      }
    }
  }
}


def create_document_index() -> None:
    """Создает индекс в Elasticsearch."""
    es_client = Elasticsearch(ES_HOST)

    while not es_client.ping():
        time.sleep(0.5)

    try:
        es_client.indices.create(
            index='document-index',
            settings=index_create_settings,
        )
    except elasticsearch.BadRequestError:
        pass

    es_client.transport.close()


def wait_connection_to_es() -> None:
    """Останавливает запуск приложения, пока не заработает Elasticsearch."""
    es_client = Elasticsearch(ES_HOST)
    while not es_client:
        time.sleep(0.5)
    es_client.transport.close()


def get_es_client() -> Elasticsearch:
    es_client = Elasticsearch(ES_HOST)
    try:
        yield es_client
    finally:
        es_client.transport.close()
