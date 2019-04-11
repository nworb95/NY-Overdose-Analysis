import modin.pandas as pd
import re
from sodapy import Socrata


def offset_data(json_string):
    """Works around default 1000 limit for reading from Socrata jsons.
    """
    if "health.data.ny" not in json_string:
        client = Socrata("data.ny.gov", None)
    else:
        client = Socrata("health.data.ny.gov", None)
    offset = 0
    limit = 1000
    dataset = re.search(r"resource/(.*).json", json_string).group(1)
    results = []
    while client.get(dataset, limit=limit, offset=offset):
        data = pd.DataFrame.from_records(
            client.get(dataset, limit=limit, offset=offset)
        )
        results.append(data)
        offset = +limit

    return pd.concat(results)
