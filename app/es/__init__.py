from app.es.tools import (
    init_es,
    ES_INDEX,
    wait_connection_to_es,
)
from app.es.queries import es_search, create_es_document, delete_es_document

from elasticsearch import AsyncElasticsearch

es_client = AsyncElasticsearch('http://elasticsearch:9200')
