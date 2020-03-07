import src.elk.utils as utils
import pandas as pd
from elasticsearch import Elasticsearch, helpers

es_client = Elasticsearch(http_compress=True)
json = pd.read_json('../../data/mental_health_data_by_county/0.json')


def doc_generator(df):
    df_gen = df.iterrows()
    for index, document in df_gen:
        yield {
            "_index": 'your_index',
            "_type": "_doc",
            "_id": f"{document['id']}",
            "_source": utils.filter_keys(document)
        }
    raise StopIteration


helpers.bulk(es_client, doc_generator(json))
