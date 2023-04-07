import elasticsearch
from elasticsearch import AsyncElasticsearch
import time

ES_INDEX = 'document-index'

es_client = AsyncElasticsearch('http://elasticsearch:9200')

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

    while not es_client.ping():
        time.sleep(0.5)

    try:
        es_client.indices.create(
            index=ES_INDEX,
            settings=index_create_settings,
        )
    except elasticsearch.BadRequestError:
        pass


def delete_document_index() -> None:
    """Удаляет индекс в Elasticsearch."""
    try:
        es_client.indices.delete(index=ES_INDEX)
    except elasticsearch.NotFoundError:
        pass


def wait_connection_to_es() -> None:
    """Останавливает запуск приложения, пока не заработает Elasticsearch."""
    while not es_client.ping():
        time.sleep(0.5)


def init_es() -> None:
    wait_connection_to_es()
    delete_document_index()
    create_document_index()
