from models import Base
from sqlalchemy import (
    Column,
    Integer,
    Text,
    String
)

class InpatientDischarges(Base):
    __tablename__ = 'countywise_inpatient_discharges'
    id = Column(Integer, primary_key=True)
    hospital_service_area = Column(String(15))
    hospital_county = Column(String(11))
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
    discharge_year = Column(Integer)
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

    def __init__(self, data):
        hospital_service_area = data.hospital_service_area
        hospital_county = data.hospital_county
        operating_certificate_number = data.operating_certificate_number
        facility_id = data.facility_id
        facility_name = data.facility_name
        age_group = data.age_group
        zip_code_3_digits = data.zip_code_3_digits
        gender = data.gender
        race = data.race
        ethnicity = data.ethnicity
        length_of_stay = data.length_of_stay
        type_of_admission = data.type_of_admission
        patient_disposition = data.patient_disposition
        discharge_year = data.discharge_year
        ccs_diagnosis_code = data.ccs_diagnosis_code
        ccs_diagnosis_description = data.ccs_diagnosis_description
        ccs_procedure_code = data.ccs_procedure_code
        ccs_procedure_description = data.ccs_procedure_description
        apr_drg_code = data.apr_drg_code
        apr_drg_description = data.apr_drg_description
        apr_mdc_code = data.apr_mdc_code
        apr_mdc_description = data.apr_mdc_description
        apr_severity_of_illness_code = data.apr_severity_of_illness_code
        apr_severity_of_illness_description = data.apr_severity_of_illness_description
        apr_risk_of_mortality = data.apr_risk_of_mortality
        apr_medical_surgical_description = data.apr_medical_surgical_description
        source_of_payment_1 = data.source_of_payment_1
        source_of_payment_2 = data.source_of_payment_2
        source_of_payment_3 = data.source_of_payment_3
        birth_weight = data.birth_weight
        abortion_edit_indicator = data.abortion_edit_indicator
        emergency_department_indicator = data.emergency_department_indicator
        total_charges = data.total_charges
        total_costs = data.total_costs