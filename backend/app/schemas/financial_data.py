from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class FinancialDataBase(BaseModel):
    """Base Pydantic schema with all common fields."""
    data_type: str
    state: Optional[str] = None
    district: Optional[str] = None
    scheme_name: Optional[str] = None
    scheme_details: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    application_process: Optional[str] = None
    required_documents: Optional[Dict[str, Any]] = None
    contact_information: Optional[Dict[str, Any]] = None
    target_beneficiaries: Optional[str] = None
    bank_name: Optional[str] = None
    loan_type: Optional[str] = None
    interest_rate: Optional[float] = None
    loan_amount_min: Optional[float] = None
    loan_amount_max: Optional[float] = None
    repayment_period: Optional[str] = None
    subsidy_percentage: Optional[float] = None
    subsidy_amount_max: Optional[float] = None
    crop_name: Optional[str] = None
    mandi_name: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    modal_price: Optional[float] = None
    arrival_quantity: Optional[float] = None
    insurance_scheme: Optional[str] = None
    premium_rate: Optional[float] = None
    sum_insured: Optional[float] = None
    coverage_period: Optional[str] = None
    effective_from: Optional[datetime] = None
    effective_until: Optional[datetime] = None
    data_source: Optional[str] = None

class FinancialDataCreate(FinancialDataBase):
    """Schema for creating a new financial data record."""
    pass

class FinancialDataInDB(FinancialDataBase):
    """Schema for reading data from the database, includes DB-generated fields."""
    id: int
    last_updated: datetime

    # For Pydantic V2, orm_mode is renamed to from_attributes
    model_config = ConfigDict(from_attributes=True)
