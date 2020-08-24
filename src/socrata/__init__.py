import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__)).rstrip("src/socrata") + "s/"

NY_OVERDOSE_DATA = ROOT_DIR + "src/socrata/assets/ny_sources.json"
NY_DATA_DIR = ROOT_DIR + "data/raw_data/"

OVERDOSE_TABLE_MAPPINGS = (
    {
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
        "juvenile_detention_by_county": {
            "year": "year",
            "population": [
                "secure_non_secure_admissions",
                "non_secure_admissions",
                "secure_non_secure_unique_youth",
                "non_secure_unique_youth",
            ],
        },
        "local_unemployment_data_by_county": {
            "year": "year",
            "month": "month",
            "population": ["laborforce", "employed", "unemployed"],
        },
        "long_term_industry_projection_by_county": {
            "year": ["base_year", "projected_year"]
        },
        "low_income_tax_credits_by_county": {
            "year": "calendar_year",
            "population": "affordable_units",
        },
        "medicaid_patient_visits_by_county": {
            "year": "year",
            "population": [
                "ip_recips",
                "ip_admits",
                "ip_admits",
                "er_recips",
                "er_visits",
            ],
        },
        "mined_land_data_by_county": {
            "year": [],
            "area": [
                "acres_controlled",
                "acres_life_of_mine",
                "acres_affected",
                "acres_reclaimed",
                "acresbb",
                "acresbb_range",
            ],
        },
        "ny_state_career_centers": {},
        "oil_gas_production_data_by_county": {"year": "year"},
        "opioid_deaths_by_county": {
            "year": "year",
            "population": "opioid_poisoning_deaths",
        },
        "overall_employment_data_by_county": {
            "year": "year",
            "population": "current_employment",
        },
        "parole_data_by_county": {"year": "snapshot_year"},
        "recidivism_data_by_county": {"year": "release_year"},
        "short_term_industry_projection_by_county": {
            "year": "period",
            "population": [
                "base_year_employment_estimate",
                "projected_year_employment_estimate",
                "net_change",
            ],
        },
        "swm_data_by_county": {"year": "expiration_date"},
        "unemployment_avg_duration_by_county": {"year": "year"},
        "union_compensation_claims_by_county": {
            "year": ["accident_date", "anrc_date", "assembly_date", "first_appeal_date"]
        },
    },
)
