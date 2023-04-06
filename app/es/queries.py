from elasticsearch import Elasticsearch

from app.es import ES_INDEX


async def es_search(query: str, es_client: Elasticsearch) -> list[dict]:
    """Возвращает поисковый ответ от ElastSearch."""
    es_query = {
        'match': {
            'text': query
        }
    }
    es_sort = {
        '_score': {
            'order': 'desc'
        }
    }

    resp = await es_client.search(
        index=ES_INDEX,
        query=es_query,
        sort=es_sort,
    )
    hits = [hit['_source'] for hit in resp['hits']['hits'][:20]]

    return hits


async def create_es_document(
        document_id: int, text: str, es_client: Elasticsearch
) -> None:
    await es_client.index(
        index=ES_INDEX,
        document={
            'id': document_id,
            'text': text
        }
    )


async def delete_es_document(
        document_id: int, es_client: Elasticsearch
) -> None:
    await es_client.delete_by_query(
        index=ES_INDEX,
        query={
            'match':
                {'id': document_id}
        }
    )
