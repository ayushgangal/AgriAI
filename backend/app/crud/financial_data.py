from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timezone
from typing import List, Optional
from app.models.financial_data import FinancialData
from app.schemas.financial_data import FinancialDataCreate

class CRUDFinancialData:
    """
    Data Access Layer for financial data.
    Contains all direct database query logic.
    """
    def get_schemes(self, db: Session, *, data_type: str, state: Optional[str] = None, active_only: bool = True) -> List[FinancialData]:
        """Generic function to get active credit, subsidy, or insurance schemes."""
        query = db.query(FinancialData).filter(FinancialData.data_type == data_type)
        
        if state:
            # Filter by specific state or where state is NULL (for central schemes)
            query = query.filter(or_(FinancialData.state == state, FinancialData.state.is_(None)))
            
        if active_only:
            now_utc = datetime.now(timezone.utc)
            query = query.filter(or_(
                FinancialData.effective_until.is_(None),
                FinancialData.effective_until > now_utc
            ))
            
        return query.all()

    def get_market_prices(self, db: Session, *, crop_name: str) -> List[FinancialData]:
        """Gets most recent market prices for a crop from the database (for historical data)."""
        return db.query(FinancialData).filter(
            FinancialData.data_type == "market_price",
            FinancialData.crop_name.ilike(f"%{crop_name}%")
        ).order_by(FinancialData.last_updated.desc()).limit(10).all()

    def create(self, db: Session, *, financial_in: FinancialDataCreate) -> FinancialData:
        """Create a new financial data entry."""
        db_obj = FinancialData(**financial_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

# Create a single, reusable instance of the CRUD class
financial_data_crud = CRUDFinancialData()
