import src.elk.utils as utils
import pandas as pd
import hashlib, json, requests
from elasticsearch import Elasticsearch, helpers


fpath = "../../data/raw_data/recidivism_data_by_county/0.json"
index = "recidivism_by_county"
elk_url = "http://localhost:9200/{}".format(index)
# data = utils.format_year_column(pd.read_json(fpath), "release_year")


def post_to_es(df, index=index, server=elk_url, chunk_size=2000):
    headers = {"content-type": "application/x-ndjson", "Accept-Charset": "UTF-8"}
    records = df.to_dict(orient="records")
    actions = [
        """{ "index" : { "_index" : "%s"} }\n""" % (index) + json.dumps(records[j])
        for j in range(len(records))
    ]
    i = 0
    while i < len(actions):
        serverAPI = server + "/_bulk"
        data = "\n".join(actions[i : min([i + chunk_size, len(actions)])])
        data = data + "\n"
        r = requests.post(serverAPI, data=data, headers=headers)
        print(r.content)
        i = i + chunk_size


def doc_generator(df, index_name):
    df_gen = df.iterrows()
    import pdb

    pdb.set_trace()
    for index, document in df_gen:
        yield {
            "_index": index_name,
            "_doc": "_doc",
            "_id": f"{index}",
            "_source": utils.filter_keys(document.to_dict(), df.columns),
        }
    raise StopIteration


def upload_socrata_data(json_path, index):
    es_client = Elasticsearch(http_compress=True)
    data = utils.format_year_column(pd.read_json(json_path), "release_year")
    doc = doc_generator(data, index)
    # return helpers.bulk(es_client, doc_generator(data, index))
    for i in doc:
        print(i)
