from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
import logging
from app.core.database import get_db
from app.services.finance_service import FinanceService
from app.schemas.financial_data import FinancialDataInDB, FinancialDataCreate
from app.routers.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/finance", tags=["Finance"])

@router.get("/schemes", response_model=Dict[str, List[FinancialDataInDB]])
def get_all_schemes(
    state: Optional[str] = Query(None, description="Filter schemes by state, e.g., 'Tamil Nadu'"),
    loan_amount_needed: Optional[float] = Query(None, description="Loan amount you need"),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Get a list of relevant financial schemes (credit and subsidy).
    Filters by state and required loan amount.
    """
    try:
        user_context = {"state": state, "loan_amount_needed": loan_amount_needed}
        service = FinanceService(db)
        schemes = service.get_schemes_info(user_context)
        return {
            "credit_schemes": schemes["credit_schemes"],
            "subsidy_schemes": schemes["subsidy_schemes"]
        }
    except Exception as e:
        logger.error(f"Error fetching schemes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Could not fetch financial schemes.")

@router.get("/market-trends/{crop_name}", response_model=Dict[str, Any])
async def get_single_crop_trend(crop_name: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Get live market trend and price prediction for a specific crop.
    """
    service = FinanceService(db)
    trends = await service.get_market_trends(crop_name)
    if "error" in trends:
        raise HTTPException(status_code=404, detail=trends["error"])
    return trends

@router.get("/market-trends", response_model=Dict[str, Any])
async def get_all_market_trends(db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Get live market trends for all available crops.
    """
    service = FinanceService(db)
    trends = await service.get_all_market_trends()
    return trends

@router.get("/loan-calculator", response_model=Dict[str, Any])
def get_loan_emi(
    loan_amount: float = Query(..., description="Total loan amount required", gt=0),
    repayment_period_months: int = Query(..., description="Loan tenure in months", gt=0),
    loan_type: str = Query(..., description="Type of loan, e.g., 'crop_loan'"),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Calculate the Estimated Monthly Installment (EMI) for a loan.
    """
    service = FinanceService(db)
    calculation = service.calculate_loan_emi(loan_amount, repayment_period_months, loan_type)
    return calculation

@router.post("/data", response_model=FinancialDataInDB, status_code=201)
def create_financial_data_entry(
    financial_in: FinancialDataCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Admin endpoint to create a new financial data entry in the database.
    """
    from app.crud.financial_data import financial_data_crud
    try:
        return financial_data_crud.create(db=db, financial_in=financial_in)
    except Exception as e:
        logger.error(f"Error creating financial data: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail="Could not create financial data entry.")
