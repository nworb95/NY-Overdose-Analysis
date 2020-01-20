import requests
import pandas as pd
from io import BytesIO
import xlrd

county_list = [
    1,
    3,
    5,
    7,
    9,
    11,
    13,
    15,
    17,
    19,
    21,
    23,
    25,
    27,
    29,
    31,
    33,
    35,
    37,
    39,
    41,
    43,
    45,
    47,
    49,
    51,
    53,
    55,
    57,
    59,
    61,
    63,
    65,
    67,
    69,
    71,
    73,
    75,
    77,
    79,
    81,
    83,
    87,
    85,
    89,
    91,
    93,
    95,
    97,
    99,
    101,
    103,
    105,
    107,
    109,
    111,
    113,
    115,
    117,
    119,
    121,
    123,
]


def get_actual_population_data():
    return pd.read_excel(
        BytesIO(
            requests.get(
                "https://labor.ny.gov/stats/nys/CO-EST00INT-01-36.xlsx"
            ).content
        ),
        skiprows=3,
    )[:-8]


def cache_actual_population_data(df):
    df.to_json("./raw_data/actual_ny_population_data.json")


def pull_actual_population_data():
    df = get_actual_population_data()
    cache_actual_population_data(df)
    return df


def get_projected_population_data(county_list):
    projection_df_list = []
    for request in county_list:
        projection_df_list.append(
            pd.read_excel(
                BytesIO(
                    requests.get(
                        "https://pad.human.cornell.edu/counties/expprojdata.cfm?county={}".format(
                            request
                        )
                    ).content
                )
            )
        )
    return pd.concat(projection_df_list)


def cache_projected_population_data(df):
    df.to_json('./raw_data/projected_ny_population_data.json')


def pull_projected_population_data(county_list):
    df = get_projected_population_data(county_list)
    cache_projected_population_data(df)
    return df
