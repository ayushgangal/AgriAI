from sqlalchemy import Column, Integer, String, DateTime, Float, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base # Use the Base from our database setup

class FinancialData(Base):
    """
    SQLAlchemy model for the 'financial_data' table.
    This unified model stores all types of financial information.
    """
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True, index=True)
    data_type = Column(String(50), nullable=False, index=True) # E.g., 'credit', 'subsidy', 'market_price'
    state = Column(String(50), index=True)
    district = Column(String(50), index=True)
    
    # Common scheme fields
    scheme_name = Column(String(200))
    scheme_details = Column(Text)
    eligibility_criteria = Column(Text)
    application_process = Column(Text)
    required_documents = Column(JSON)
    contact_information = Column(JSON)
    target_beneficiaries = Column(String(200))
    
    # Credit specific
    bank_name = Column(String(100))
    loan_type = Column(String(50), index=True)
    interest_rate = Column(Float)
    loan_amount_min = Column(Float)
    loan_amount_max = Column(Float)
    repayment_period = Column(String(50))
    
    # Subsidy specific
    subsidy_percentage = Column(Float)
    subsidy_amount_max = Column(Float)
    
    # Market price specific
    crop_name = Column(String(100), index=True)
    mandi_name = Column(String(100))
    min_price = Column(Float)
    max_price = Column(Float)
    modal_price = Column(Float)
    arrival_quantity = Column(Float)
    
    # Insurance specific
    insurance_scheme = Column(String(100))
    premium_rate = Column(Float)
    sum_insured = Column(Float)
    coverage_period = Column(String(100))

    # Timestamps
    effective_from = Column(DateTime(timezone=True))
    effective_until = Column(DateTime(timezone=True))
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    data_source = Column(String(100))

    def __repr__(self):
        return f"<FinancialData(id={self.id}, type='{self.data_type}', name='{self.scheme_name or self.crop_name}')>"
