import src.elk.utils as utils
import pandas as pd
import hashlib
from elasticsearch import Elasticsearch, helpers


def doc_generator(df, index_name, doc_name):
    df_gen = df.iterrows()
    for index, document in df_gen:
        yield {
            "_index": index_name,
            "_doc": doc_name,  # or doc??
            "_id": f"{hashlib.sha1(doc_name.encode()).hexdigest() + '_' + str(index)}",
            "_source": utils.filter_keys(document.to_dict(), df.columns)
        }
    raise StopIteration


def upload_socrata_data(json_path, index, document):
    es_client = Elasticsearch(http_compress=True)
    data = utils.format_year_column(pd.read_json(json_path), 'service_year')
    return helpers.bulk(es_client, doc_generator(data, index, document))
