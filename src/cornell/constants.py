PROJECTED_DROP_COLUMNS = [
    "COUNTY",
    "SEXCODE",
    "SEX_DESCR",
    "AGEGRPCODE",
    "AGEGRP_DESCR",
    "RACECODE",
    "RACE_DESCR",
]
HISTORICAL_POPULATION_COLUMNS = {
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
PROJECTED_POPULATION_COLUMNS = {
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
MISSING_POPULATION_YEARS = ["2011", "2012", "2013", "2014"]
COUNTY_LIST = [
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
HISTORICAL_DATA_URL = "https://labor.ny.gov/stats/nys/CO-EST00INT-01-36.xlsx"
PROJECTED_DATA_UNFORMATTED_URL = (
    "https://pad.human.cornell.edu/counties/expprojdata.cfm?county={}"
)
HISTORICAL_POPULATION_DATA_CACHE = (
    "data/cornell_population_data/historical_ny_population_data.json"
)
PROJECTED_POPULATION_DATA_CACHE = (
    "data/cornell_population_data/projected_ny_population_data.json"
)
