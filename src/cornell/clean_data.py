import pandas as pd


def clean_actual_population_data(df):
    df = df.rename(
        columns={
            "Unnamed: 0": "County",
            "Unnamed: 13": "2010",
            2000: "2000",
            2001: "2001",
            2002: "2002",
            2003: "2003",
            2004: "2004",
            2005: "2005",
            2006: "2006",
            2007: "2007",
            2008: "2008",
            2009: "2009",
        }
    ).drop(["Unnamed: 1", "Unnamed: 12"], axis=1)
    df["County"] = df["County"].str.replace(".", "")
    return df[~(df["County"] == "New York")]


def clean_projected_population_data(df):
    filtered_df = df[(df["SEX_DESCR"] == "All") & (df["AGEGRP_DESCR"] == "Total")]
    clean_df = filtered_df.rename(
        columns={
            "COUNTY_DESCR": "County",
            "YR_2015": "2015",
            "YR_2016": "2016",
            "YR_2017": "2017",
            "YR_2018": "2018",
            "YR_2019": "2019",
            "YR_2020": "2020",
            "YR_2021": "2021",
            "YR_2022": "2022",
            "YR_2023": "2023",
            "YR_2024": "2024",
            "YR_2025": "2025",
            "YR_2026": "2026",
            "YR_2027": "2027",
            "YR_2028": "2028",
            "YR_2029": "2029",
            "YR_2030": "2030",
            "YR_2031": "2031",
            "YR_2032": "2032",
            "YR_2033": "2033",
            "YR_2034": "2034",
            "YR_2035": "2035",
            "YR_2036": "2036",
            "YR_2037": "2037",
            "YR_2038": "2038",
            "YR_2039": "2039",
            "YR_2040": "2040",
        }
    ).drop(
        [
            "COUNTY",
            "SEXCODE",
            "SEX_DESCR",
            "AGEGRPCODE",
            "AGEGRP_DESCR",
            "RACECODE",
            "RACE_DESCR",
        ],
        axis=1,
    )
    clean_df["County"] = clean_df["County"] + " County"
    return clean_df.reset_index().drop(["index"], axis=1)


def merge_population_data(actual_df, projected_df):
    df = pd.merge(actual_df, projected_df, on="County")
    cols = [x for x in df.columns.tolist() if x != "County"]
    for i in cols:
        df[i] = df[i].astype(int)
    missing_years = ["2011", "2012", "2013", "2014"]
    big_df = pd.concat([df, pd.DataFrame(columns=missing_years)], sort=False)
    for year in missing_years:
        big_df[year] = pd.to_numeric(big_df[year], errors="coerce")
    interpolate_df = big_df.drop("County", axis=1)
    interpolated_df = interpolate_df.interpolate(method="akima", axis=1)
    for year in missing_years:
        interpolated_df[year] = interpolated_df[year].astype(float)
    return pd.concat([big_df["County"], interpolated_df], axis=1)
