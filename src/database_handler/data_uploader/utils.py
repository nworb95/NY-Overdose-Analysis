from datetime import datetime

import dateutil.parser
import pandas as pd
from database_handler.data_uploader.constants import SOCRATA_KEY_COLUMNS


def split_industry_projection_periods(period: str):
    split_period = period.split("-")
    return split_period[0].strip(), split_period[1].strip()


def parse_date_to_year(date: str):
    # TODO refactor this nonsense
    try:
        return datetime.strptime(date, "%b-%y").strftime("%Y")
    except ValueError:
        try:
            return datetime.strptime(date, "%B-%y").strftime("%Y")
        except ValueError:
            return dateutil.parser.parse(str(date)).strftime("%Y")
        except TypeError:
            return dateutil.parser.parse(str(date)).strftime("%Y")
    except TypeError:
        return dateutil.parser.parse(str(date)).strftime("%Y")


def standardize_year_column(socrata_data: pd.DataFrame, socrata_dataset: str):
    if socrata_dataset in (
        "long_term_industry_projection_by_county",
        "short_term_industry_projection_by_county",
    ):
        socrata_data[["start_period", "end_period"]] = (
            socrata_data["period"].apply(split_industry_projection_periods).tolist()
        )
    if socrata_dataset == "swm_data_by_count":
        socrata_data["expiration_year"] = socrata_data["expiration_date"].apply(
            lambda a: a if a is None else dateutil.parser.parse(a).strftime("%Y")
        )
    if "year" not in socrata_data.columns:
        # if year not in columns, extract year from the first date-type column
        if SOCRATA_KEY_COLUMNS[socrata_dataset]["year"]:
            socrata_data["year"] = (
                socrata_data[SOCRATA_KEY_COLUMNS[socrata_dataset]["year"]]
                .iloc[:, 0]
                .apply(parse_date_to_year)
            )
    if "year" in socrata_data.columns:
        socrata_data.year = socrata_data.year.astype(int)
    return socrata_data


def standardize_county_column(socrata_data: pd.DataFrame):
    if "County" in socrata_data.columns:
        socrata_data.county = socrata_data["County"].str.title()
    if "county" not in socrata_data.columns:
        pass
    elif not socrata_data["county"].str.contains(" County").any():
        socrata_data.county = socrata_data.county.str.title() + " County"
    return socrata_data
