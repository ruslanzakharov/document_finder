import elasticsearch
from elasticsearch import AsyncElasticsearch
import time

ES_INDEX = 'document-index'

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


async def create_document_index(es_client: AsyncElasticsearch) -> None:
    """Создает индекс в Elasticsearch."""
    try:
        await es_client.indices.create(
            index=ES_INDEX,
            settings=index_create_settings,
        )
    except elasticsearch.BadRequestError:
        pass


async def delete_document_index(es_client: AsyncElasticsearch) -> None:
    """Удаляет индекс в Elasticsearch."""
    try:
        await es_client.indices.delete(index=ES_INDEX)
    except elasticsearch.NotFoundError:
        pass


async def wait_connection_to_es(es_client: AsyncElasticsearch) -> None:
    """Останавливает запуск приложения, пока не заработает Elasticsearch."""
    while not await es_client.ping():
        time.sleep(0.5)


async def init_es(es_client: AsyncElasticsearch) -> None:
    await wait_connection_to_es(es_client)
    await delete_document_index(es_client)
    await create_document_index(es_client)
