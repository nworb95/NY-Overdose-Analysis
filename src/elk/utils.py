from datetime import datetime
import pandas as pd
import dateutil


def safe_date(date_value):
    return (
        pd.to_datetime(date_value)
        if not pd.isna(date_value)
        else datetime(1970, 1, 1, 0, 0)
    )


def safe_value(field_val):
    return field_val if not pd.isna(field_val) else "Other"


def filter_keys(document, use_these_keys):
    return {key: document[key] for key in use_these_keys}


def format_year_column(data, column_name):
    data[column_name] = data[column_name].apply(lambda x: dateutil.parser.parse(str(x)))
    return data
