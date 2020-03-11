NY_OVERDOSE_DATA = "data/ny_sources.json"
TEST_OVERDOSE_DATA = "../ny_sources.json"

overdose_table_mappings = {
    "active_construction_by_county": {
        "year": ["construction_completion_date", "construction_start_date"]
    },
    "adult_arrest_data_by_county": {
        "year": "year",
        "population": [
            "total",
            "felony_total",
            "drug_felony",
            "vionet_felony",
            "dwi_felony",
            "other_felony",
            "misdemeanor_total",
            "drug_misd",
            "dwi_misd",
            "property_misd",
            "other_misd",
        ],
    },
    "employment_data_by_race_by_county": {"year": "year"},
    "employment_wage_data_by_county": {
        "year": "year",
        "population": "average_employment",
    },
    "foster_child_data_by_county": {
        "year": "year",
        "population": [
            "adoptive_home",
            "agency_operated_boarding_home",
            "approved_relative_home",
            "foster_boarding_home",
            "group_home",
            "group_residence",
            "institution",
            "supervised_independent_living",
            "other",
            "total_days_in_care",
            "admissions",
            "discharges",
            "children_in_care",
            "number_of_children_served",
            "indicated_cps_reports",
        ],
    },
    "inpatient_discharges_by_county": {"year": "discharge_year"},
    "jail_population_by_county": {
        "year": "year",
        "population": [
            "census_2",
            "boarded_out",
            "boarded_in",
            "census",
            "sentenced",
            "civil",
            "federal",
            "technical_parole_violators",
            "state_readies",
            "other_unsentenced",
        ],
    },
}
