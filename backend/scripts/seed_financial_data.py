#!/usr/bin/env python3
"""
Script to seed the database with initial financial data
"""

import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.crud.financial_data import financial_data_crud
from app.schemas.financial_data import FinancialDataCreate

def seed_financial_data():
    """Seed the database with initial financial data"""
    db = SessionLocal()
    
    try:
        # Credit schemes
        credit_schemes = [
            {
                "data_type": "credit",
                "scheme_name": "Kisan Credit Card",
                "bank_name": "All Scheduled Banks",
                "loan_type": "crop_loan",
                "interest_rate": 7.0,
                "loan_amount_min": 10000.0,
                "loan_amount_max": 300000.0,
                "repayment_period": "1 year",
                "eligibility_criteria": "All farmers with land ownership",
                "scheme_details": "Easy credit facility for farmers",
                "application_process": "Visit nearest bank branch with required documents",
                "required_documents": {"documents": ["land documents", "aadhaar", "bank account"]},
                "contact_information": {
                    "primary": "Nearest bank branch",
                    "helpline": "1800-XXX-XXXX",
                    "website": "https://www.nabard.org"
                },
                "effective_from": datetime.now(),
                "effective_until": datetime.now() + timedelta(days=365),
                "data_source": "NABARD"
            },
            {
                "data_type": "credit",
                "scheme_name": "PM-KISAN",
                "bank_name": "Government of India",
                "loan_type": "direct_benefit",
                "interest_rate": 0.0,
                "loan_amount_min": 6000.0,
                "loan_amount_max": 6000.0,
                "repayment_period": "N/A",
                "eligibility_criteria": "Small and marginal farmers",
                "scheme_details": "Direct income support to farmers",
                "application_process": "Register on PM-KISAN portal",
                "required_documents": {"documents": ["aadhaar", "land documents", "bank account"]},
                "contact_information": {
                    "primary": "PM-KISAN Helpline",
                    "helpline": "155261",
                    "website": "https://pmkisan.gov.in"
                },
                "effective_from": datetime.now(),
                "effective_until": datetime.now() + timedelta(days=365),
                "data_source": "Government of India"
            }
        ]
        
        # Subsidy schemes
        subsidy_schemes = [
            {
                "data_type": "subsidy",
                "scheme_name": "PM Fasal Bima Yojana",
                "subsidy_percentage": 90.0,
                "subsidy_amount_max": 10000.0,
                "target_beneficiaries": "All farmers",
                "scheme_details": "Crop insurance scheme with government subsidy",
                "application_process": "Contact insurance company or bank",
                "required_documents": {"documents": ["crop details", "land documents"]},
                "contact_information": {
                    "primary": "Insurance companies",
                    "helpline": "1800-XXX-XXXX",
                    "website": "https://pmfby.gov.in"
                },
                "effective_from": datetime.now(),
                "effective_until": datetime.now() + timedelta(days=365),
                "data_source": "Government of India"
            },
            {
                "data_type": "subsidy",
                "scheme_name": "Soil Health Card Scheme",
                "subsidy_percentage": 100.0,
                "subsidy_amount_max": 500.0,
                "target_beneficiaries": "All farmers",
                "scheme_details": "Free soil testing and recommendations",
                "application_process": "Contact agriculture department",
                "required_documents": {"documents": ["soil sample"]},
                "contact_information": {
                    "primary": "Agriculture Department",
                    "helpline": "1800-XXX-XXXX",
                    "website": "https://soilhealth.dac.gov.in"
                },
                "effective_from": datetime.now(),
                "effective_until": datetime.now() + timedelta(days=365),
                "data_source": "Agriculture Department"
            }
        ]
        
        # Market prices
        market_prices = [
            {
                "data_type": "market_price",
                "crop_name": "rice",
                "mandi_name": "Delhi",
                "min_price": 1750.0,
                "max_price": 1850.0,
                "modal_price": 1800.0,
                "arrival_quantity": 5000.0,
                "scheme_details": "Current market prices for rice",
                "effective_from": datetime.now(),
                "effective_until": datetime.now() + timedelta(days=7),
                "data_source": "Agricultural Market Information System"
            },
            {
                "data_type": "market_price",
                "crop_name": "wheat",
                "mandi_name": "Punjab",
                "min_price": 2050.0,
                "max_price": 2150.0,
                "modal_price": 2100.0,
                "arrival_quantity": 3000.0,
                "scheme_details": "Current market prices for wheat",
                "effective_from": datetime.now(),
                "effective_until": datetime.now() + timedelta(days=7),
                "data_source": "Agricultural Market Information System"
            },
            {
                "data_type": "market_price",
                "crop_name": "maize",
                "mandi_name": "Madhya Pradesh",
                "min_price": 1450.0,
                "max_price": 1550.0,
                "modal_price": 1500.0,
                "arrival_quantity": 2000.0,
                "scheme_details": "Current market prices for maize",
                "effective_from": datetime.now(),
                "effective_until": datetime.now() + timedelta(days=7),
                "data_source": "Agricultural Market Information System"
            }
        ]
        
        # Insurance schemes
        insurance_schemes = [
            {
                "data_type": "insurance",
                "insurance_scheme": "PM Fasal Bima Yojana",
                "premium_rate": 1.5,
                "sum_insured": 50000.0,
                "coverage_period": "crop_cycle",
                "scheme_details": "Comprehensive crop insurance coverage",
                "application_process": "Enroll during sowing period",
                "required_documents": {"documents": ["crop details", "land documents"]},
                "contact_information": {
                    "primary": "Insurance companies",
                    "helpline": "1800-XXX-XXXX",
                    "website": "https://pmfby.gov.in"
                },
                "effective_from": datetime.now(),
                "effective_until": datetime.now() + timedelta(days=365),
                "data_source": "Government of India"
            }
        ]
        
        # Insert all data
        all_data = credit_schemes + subsidy_schemes + market_prices + insurance_schemes
        
        for data in all_data:
            financial_in = FinancialDataCreate(**data)
            financial_data_crud.create(db, financial_in=financial_in)
        
        print(f"Successfully seeded {len(all_data)} financial data records")
        
    except Exception as e:
        print(f"Error seeding financial data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_financial_data() 