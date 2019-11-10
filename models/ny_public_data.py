from models import Base
from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    Date
)

# TODO get some unemployment data... and more health data


class InpatientDischarges(Base):
    __tablename__ = 'countywise_inpatient_discharges'
    id = Column(Integer, primary_key=True)
    hospital_county = Column(String(11))
    discharge_year = Column(Integer)
    hospital_service_area = Column(String(15))
    operating_certificate_number = Column(String(8))
    facility_id = Column(Integer)
    facility_name = Column(String(70))
    age_group = Column(String(11))
    zip_code_3_digits = Column(String(3), nullable=True)
    gender = Column(String(1))
    race = Column(String(32))
    ethnicity = Column(String(20))
    length_of_stay = Column(String(5))
    type_of_admission = Column(String(15))
    patient_disposition = Column(String(37))
    ccs_diagnosis_code = Column(String(3))
    ccs_diagnosis_description = Column(String(450))
    ccs_procedure_code = Column(String(3))
    ccs_procedure_description = Column(String(450))
    apr_drg_code = Column(String(3))
    apr_drg_description = Column(String(89))
    apr_mdc_code = Column(String(2))
    apr_mdc_description = Column(String(200))
    apr_severity_of_illness_code = Column(String(1))
    apr_severity_of_illness_description = Column(String(8))
    apr_risk_of_mortality = Column(String(8))
    apr_medical_surgical_description = Column(String(14))
    source_of_payment_1 = Column(String(25))
    source_of_payment_2 = Column(String(25))
    source_of_payment_3 = Column(String(25))
    birth_weight = Column(String(4))
    abortion_edit_indicator = Column(String(1))
    emergency_department_indicator = Column(String(1))
    total_charges = Column(String(12))
    total_costs = Column(String(12))


class MedicaidPatientVisits(Base):
    __tablename__ = 'countywise_medicaid_patient_visits'
    id = Column(Integer, primary_key=True)
    county = Column(String)
    year = Column(Integer)
    dual_status = Column(String)
    major_diagnostic_category = Column(String)
    episode_disease_category = Column(String)
    er_recips = Column(Integer)
    er_visits = Column(Integer)
    ip_admits = Column(Integer)
    ip_recips = Column(Integer)
    recip_condition = Column(Integer)


class OpioidDeaths(Base):
    __tablename__ = 'countywise_opioid_deaths'
    id = Column(Integer, primary_key=True)
    county = Column(String)
    year = Column(Integer)
    opioid_poisoning_deaths = Column(Integer)


class UnionClaims(Base):
    __tablename__ = 'countywise_union_compensation_claims'
    claim_identifier = Column(Integer, primary_key=True)
    district_name = Column(String)
    accident_date = Column(Date)
    claim_type = Column(String)
    average_weekly_wage = Column(Numeric)
    current_claim_status = Column(String)
    claim_injury_type = Column(String)
    age_at_injury = Column(Integer)
    assembly_date = Column(Date)
    ancr_date = Column(Date)
    ppd_non_scheduled_loss_date = Column(Date)
    first_appeal_date = Column(Date)
    wcio_pob_desc = Column(String)
    wcio_nature_of_injury_desc = Column(String)
    wcio_cause_of_injury_desc = Column(String)
    oiics_pob_desc = Column(String)
    oiics_nature_injury_desc = Column(String)
    oiics_injury_source_desc = Column(String)
    oiics_event_exposure_desc = Column(String)
    oiics_secondary_source_desc = Column(String)
    alternative_dispute_resolution = Column(String)
    gender = Column(String)
    birth_year = Column(Integer)
    zip_code = Column(Integer)
    medical_fee_region = Column(String)
    c2_date = Column(Date)
    first_hearing_date = Column(Date)
    highest_process = Column(String)
    hearing_count = Column(Integer)
    closed_count = Column(Integer)
    atty_rep_ind = Column(String)
    carrier_name = Column(String)
    carrier_type = Column(String)
    ime4_count = Column(String)
    interval_assembled_to_ancr = Column(String)
    accident_ind = Column(String)
    occupational_disease_ind = Column(String)
    injured_in_county_name = Column(String)
    controverted_date = Column(Date)
    ppd_scheduled_loss_date = Column(Date)
    c3_date = Column(Date)
    section_32_date = Column(Date)
    ptd_date = Column(Date)


class SolidWasteManagement(Base):
    __tablename__ = 'countywise_swm_registry'
    id = Column(Integer, primary_key=True)
    state = Column(String)
    county = Column(String)
    location_city = Column(String)
    facility_name = Column(String)
    location_address = Column(String)
    zip_code = Column(Integer)
    region = Column(String)
    phone_number = Column(String)
    owner_name = Column(String)
    owner_type = Column(String)
    activity_desc = Column(String)
    active = Column(String)
    waste_types = Column(String)
    regulatory_status = Column(String)
    authorization_issue_date = Column(Date)
    expiration_date = Column(Date)


class UnemploymentDuration(Base):
    __tablename__ = 'countywise_unemployment_duration'
    id = Column(Integer, primary_key=True)
    county = Column(String)
    region = Column(String)
    year = Column(Integer)
    month = Column(Integer)
    average_duration = Column(Numeric)


class ActiveConstruction(Base):
    __tablename__ = 'countywise_active_construction'
    projectid = Column(Integer, primary_key=True)
    county = Column(String)
    construction_start_date = Column(Date)
    construction_completion_date = Column(Date)
    institution = Column(String)
    description = Column(String)
    architect = Column(String)
    construction_manager = Column(String)
    project_budget = Column(Integer)
    snapshotdate = Column(Date)


class CareerCenters(Base):
    __tablename__ = 'countywise_career_centers'
    id = Column(Integer, primary_key=True)
    state = Column(String)
    county = Column(String)
    name = Column(String)
    city = Column(String)
    street_address = Column(String)
    zip = Column(Integer)


class LowIncomeTaxCredits(Base):
    __tablename__ = 'countywise_low_income_tax_credits'
    project_number = Column(Integer, primary_key=True)
    county = Column(String)
    municipality = Column(String)
    calendar_year = Column(Integer)
    hcr_project_type = Column(String)
    project_name = Column(String)
    developer_name = Column(String)
    total_project_cost = Column(Integer)
    total_units = Column(Integer)
    affordable_units = Column(Integer)


class WageData(Base):
    __tablename__ = 'countywise_employment_wage_data'
    id = Column(Integer, primary_key=True)
    area_type = Column(String)
    area = Column(String)
    year = Column(Integer)
    naics = Column(Integer)
    naics_title = Column(String)
    establishments = Column(Integer)
    average_employment = Column(Integer)
    total_wage = Column(Integer)
    annual_average_salary = Column(Integer)


class OverallEmployment(Base):
    __tablename__ = 'countywise_overall_employment_data'
    id = Column(Integer, primary_key=True)
    area_name = Column(String)
    year = Column(Integer)
    month = Column(Integer)
    current_employment = Column(Integer)
    series = Column(Integer)
    title = Column(String)


class LongTermIndustryProjection(Base):
    __tablename__ = 'countywise_long_term_industry_production_data'
    id = Column(Integer, primary_key=True)
    area = Column(String)
    period = Column(String)
    industry_title = Column(String)
    base_year = Column(Integer)
    projected_year = Column(Integer)
    net_change = Column(Integer)
    annual_growth_rate = Column(Numeric)

class ShortTermIndustryProjection(Base):
    __tablename__ = 'countywise_short_term_industry_production_data'
    id = Column(Integer, primary_key=True)
    area = Column(String)
    period = Column(String)
    industry_title = Column(String)
    base_year_employment_estimate = Column(Integer)
    projected_year_employment_estimate = Column(Integer)
    net_change = Column(Integer)
    annual_growth_rate = Column(Numeric)


class LocalUnemployment(Base):
    __tablename__ = 'countywise_unemployment_data'
    id = Column(Integer, primary_key=True)
    area = Column(String)
    year = Column(Integer)
    month = Column(Integer)
    laborforce = Column(Integer)
    employed = Column(Integer)
    unemployed = Column(Integer)
    unemployment_rate = Column(Numeric)


class RacialEmployment(Base):
    __tablename__ = 'countywise_employment_data_by_ratio'
    id = Column(Integer, primary_key=True)
    region = Column(String)
    year = Column(Integer)
    total_population_16_years_and_older = Column(Integer)
    total_civilian_labor_force = Column(Integer)
    total_unemployed = Column(Integer)
    total_unemployment_rate = Column(Numeric)
    white_alone_population_16_years_and_older = Column(Integer)
    white_alone_civilian_labor_force = Column(Integer)
    white_alone_unemployed = Column(Integer)
    white_alone_unemployment_rate = Column(Numeric)
    black_or_african_american_alone_population_16_years_and_older = Column(Integer)
    black_or_african_american_alone_civilian_labor_force = Column(Integer)
    black_or_african_american_alone_unemployed = Column(Integer)
    black_or_african_american_alone_unemployment_rate = Column(Numeric)
    asian_alone_population_16_years_and_older = Column(Integer)
    asian_alone_civilian_labor_force = Column(Integer)
    hispanic_or_latino_population_16_years_and_older = Column(Integer)
    hispanic_or_latino_civilian_labor_force = Column(Integer)
    hispanic_or_latino_unemployed = Column(Integer)
    hispanic_or_latino_unemployment_rate = Column(Numeric)
    asian_alone_unemployed = Column(Integer)
    asian_alone_unemployment_rate = Column(Numeric)


class SUNYData(Base):
