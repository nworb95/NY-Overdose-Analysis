import pandas as pd
import logging

from src.cornell.constants import (
    CORNELL_PROJECTED_DROP_COLUMNS,
    CORNELL_HISTORICAL_POPULATION_COLUMNS,
    CORNELL_PROJECTED_POPULATION_COLUMNS,
    CORNELL_MISSING_POPULATION_YEARS,
)


def clean_historical_population_data(df: pd.DataFrame):
    """Cleans historical population data from Cornell.  Excludes
    New York City.

    Args:
        df (pd.DataFrame): dirty data

    Returns:
        pd.DataFrame: clean data
    """
    logging.info("Cleaning historical data!")
    df = df.rename(columns=CORNELL_HISTORICAL_POPULATION_COLUMNS).drop(
        ["Unnamed: 1", "Unnamed: 12"], axis=1
    )
    df["County"] = df["County"].str.replace(".", "")
    return df[~(df["County"] == "New York")]


def clean_projected_population_data(df: pd.DataFrame):
    """Cleans projected population data from Cornell.
    Filters to the all-genders and ages bucket.

    Args:
        df (pd.DataFrame): dirty data

    Returns:
        pd.DataFrame: clean data
    """

    logging.info("Cleaning projected data!")
    filtered_df = df[(df["SEX_DESCR"] == "All") & (df["AGEGRP_DESCR"] == "Total")]
    clean_df = filtered_df.rename(columns=CORNELL_PROJECTED_POPULATION_COLUMNS).drop(
        CORNELL_PROJECTED_DROP_COLUMNS, axis=1,
    )
    clean_df["County"] = clean_df["County"] + " County"
    return clean_df.reset_index().drop(["index"], axis=1)


def format_population_data(merged_df: pd.DataFrame):
    """
    Formats population dataframe by only grabbing
    :param merged_df:
    :return:
    """
    cols = [x for x in merged_df.columns.tolist() if x != "County"]
    for i in cols:
        merged_df[i] = merged_df[i].astype(int)
    return merged_df


def interpolate_missing_data(formatted_df: pd.DataFrame):
    """

    :param formatted_df:
    :return:
    """
    big_df = pd.concat([formatted_df, pd.DataFrame(columns=CORNELL_MISSING_POPULATION_YEARS)], sort=False)
    for year in CORNELL_MISSING_POPULATION_YEARS:
        big_df[year] = pd.to_numeric(big_df[year], errors="coerce")
    interpolate_df = big_df.drop("County", axis=1)
    interpolated_df = interpolate_df.interpolate(method="akima", axis=1)
    for year in CORNELL_MISSING_POPULATION_YEARS:
        interpolated_df[year] = interpolated_df[year].astype(float)
    full_df = pd.concat([big_df["County"], interpolated_df], axis=1)
    return full_df


def merge_population_data(historical_df: pd.DataFrame, projected_df: pd.DataFrame):
    """Merges historical and projected population dataframes.

    Args:
        historical_df (pd.DataFrame): clean historical data
        projected_df (pd.DataFrame): clean projected data

    Returns:
        pd.DataFrame: clean population data
    """
    df = pd.merge(historical_df, projected_df, on="County")
    formatted_df = format_population_data(df)
    interpolated_df = interpolate_missing_data(formatted_df)
    return interpolated_df
