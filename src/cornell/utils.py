import pandas as pd
import numpy as np
import logging

from cornell.constants import (
    PROJECTED_DROP_COLUMNS,
    HISTORICAL_POPULATION_COLUMNS,
    PROJECTED_POPULATION_COLUMNS,
    MISSING_POPULATION_YEARS,
)


def clean_historical_population_data(df: pd.DataFrame):
    """
    Cleans historical population data from Cornell.  Excludes
    New York City.
    :param df: dirty data
    :return: clean data
    """
    logging.info("Cleaning historical data!")
    df = df.rename(columns=HISTORICAL_POPULATION_COLUMNS).drop(
        ["Unnamed: 1", "Unnamed: 12"], axis=1
    )
    df["County"] = df["County"].str.replace(".", "")
    return df[~(df["County"] == "New York")]


def clean_projected_population_data(df: pd.DataFrame):
    """
    Cleans projected population data from Cornell.
    Filters to the all-genders and ages bucket.
    :param df: dirty data
    :return: clean data
    """
    logging.info("Cleaning projected data!")
    filtered_df = df[(df["SEX_DESCR"] == "All") & (df["AGEGRP_DESCR"] == "Total")]
    clean_df = filtered_df.rename(columns=PROJECTED_POPULATION_COLUMNS).drop(
        PROJECTED_DROP_COLUMNS, axis=1,
    )
    clean_df["County"] = clean_df["County"] + " County"
    return clean_df.reset_index().drop(["index"], axis=1)


def format_population_data(merged_df: pd.DataFrame):
    """
    Formats population dataframe by only grabbing the counties and not
    the 'County' column.
    :param merged_df: unformatted data
    :return: formatted data
    """
    cols = [x for x in merged_df.columns.tolist() if x != "County"]
    for i in cols:
        merged_df[i] = merged_df[i].astype(int)
    return merged_df


def transpose_data_for_interpolation(sorted_df: pd.DataFrame):
    """
    Transposes the data for interpolation.
    This is a silly workaround because I didn't feel like debugging scipy.
    :param sorted_df: population data sorted by year
    :return: transposed + sorted population data
    """
    transpose_df = sorted_df.transpose()
    transpose_df.columns = transpose_df.iloc[-1]
    transpose_df = transpose_df.iloc[:-1]
    for col in transpose_df:
        transpose_df[col] = pd.to_numeric(transpose_df[col], errors="coerce")
    transpose_df.index = transpose_df.index.map(np.datetime64)
    return transpose_df


def interpolate_missing_data(formatted_df: pd.DataFrame):
    """
    Interpolates missing population data with the akima spline method
    :param formatted_df: population data with missing years
    :return: complete population data
    """
    big_df = pd.concat(
        [formatted_df, pd.DataFrame(columns=MISSING_POPULATION_YEARS)], sort=False
    )
    for year in MISSING_POPULATION_YEARS:
        big_df[year] = pd.to_numeric(big_df[year], errors="coerce")
    sorted_df = big_df[big_df.columns.sort_values()]
    transpose_df = transpose_data_for_interpolation(sorted_df)
    interpolated_df = transpose_df.interpolate(method="akima")
    interpolated_df.index = interpolated_df.index.strftime("%Y")
    interpolated_df = interpolated_df.transpose()
    for year in MISSING_POPULATION_YEARS:
        interpolated_df[year] = interpolated_df[year].astype(float)
    return interpolated_df


def merge_population_data(historical_df: pd.DataFrame, projected_df: pd.DataFrame):
    """
    Merges historical and projected population dataframes.
    :param historical_df: historical population data
    :param projected_df: projected population data
    :return: merged population data
    """
    logging.info("Merging population data!")
    df = pd.merge(historical_df, projected_df, on="County")
    formatted_df = format_population_data(df)
    interpolated_df = interpolate_missing_data(formatted_df)
    return interpolated_df
