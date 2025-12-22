import logging
import httpx
import feedparser
import yfinance as yf
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from app.crud.financial_data import financial_data_crud

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# 1. REAL MARKET CLIENT (Calibrated for India)
# ---------------------------------------------------------
class MarketApiClient:
    def __init__(self):
        # Global Tickers mapped to Crops
        self.tickers = {
            "wheat": "ZW=F",      # Chicago Wheat Futures
            "rice": "ZR=F",       # Rough Rice Futures
            "cotton": "CT=F",     # Cotton Futures
            "maize": "ZC=F",      # Corn Futures
            "sugarcane": "SB=F",  # Sugar #11 (Proxy for Cane)
            "soybean": "ZS=F"     # Soybean Futures
        }
        self.currency_ticker = "INR=X" # Live USD to INR

    async def get_market_prices(self, crop: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetches LIVE data and calibrates it for Indian Mandi rates.
        """
        try:
            # 1. Fetch Live USD-INR Rate
            usd_inr = self._get_live_price(self.currency_ticker)
            if not usd_inr or usd_inr < 50: usd_inr = 84.0 # Safety fallback
            
            real_data = {}
            # If crop is provided, fetch only that. If None, fetch ALL.
            target_crops = {crop: self.tickers[crop]} if crop and crop in self.tickers else self.tickers

            for crop_name, ticker in target_crops.items():
                raw_price = self._get_live_price(ticker)
                
                if raw_price > 0:
                    # 2. Convert to Indian Rupees per Quintal (Corrected Math)
                    price_inr = self._convert_and_calibrate(crop_name, raw_price, usd_inr)
                    
                    real_data[crop_name] = {
                        "current_price": int(price_inr),
                        "unit": "quintal",
                        "trend": self._get_live_trend(ticker),
                        "last_updated": "Live"
                    }
            return real_data

        except Exception as e:
            logger.error(f"Market Data Error: {e}")
            return {}

    def _get_live_price(self, ticker: str) -> float:
        try:
            return yf.Ticker(ticker).fast_info.last_price or 0.0
        except:
            return 0.0

    def _get_live_trend(self, ticker: str) -> str:
        try:
            hist = yf.Ticker(ticker).history(period="2d")
            if len(hist) >= 2:
                return "rising" if hist['Close'].iloc[-1] > hist['Close'].iloc[-2] else "falling"
        except:
            pass
        return "stable"

    def _convert_and_calibrate(self, crop: str, raw_price: float, usd_inr: float) -> float:
        """
        Fixes the 'Cents' bug and calibrates Global Price -> Indian Mandi Price.
        """
        base_inr = 0.0
        
        # --- FIX: Added 'rice' to this list (It is quoted in CENTS, not Dollars) ---
        if crop in ["wheat", "maize", "soybean", "rice"]:
            # Price is in CENTS. Divide by 100.
            dollars = raw_price / 100.0
            
            if crop == "maize":
                factor = 3.93 # Bushels to Quintal
            elif crop == "rice":
                factor = 2.20 # Cwt to Quintal
            else:
                factor = 3.67 # Wheat/Soy Bushels to Quintal (approx)

            base_inr = dollars * usd_inr * factor
            
        elif crop == "cotton":
            # Price is in CENTS/Lb.
            dollars = raw_price / 100.0
            base_inr = dollars * usd_inr * 220.46
            
        elif crop == "sugarcane":
            # Price is CENTS/Lb (Sugar). 
            dollars = raw_price / 100.0
            base_inr = dollars * usd_inr * 220.46 

        # Step B: Calibrate to Indian Reality (MSP & Local Factors)
        calibration_factors = {
            "wheat": 1.45,     
            "rice": 1.05,      
            "maize": 1.50,     
            "soybean": 1.40,   
            "cotton": 0.55,    
            "sugarcane": 0.09 
        }
        
        return base_inr * calibration_factors.get(crop, 1.0)


# ---------------------------------------------------------
# 2. FINANCE SERVICE (With the Missing Method Added)
# ---------------------------------------------------------
class FinanceService:
    def __init__(self, db: Session):
        self.db = db
        self.crud = financial_data_crud
        self.market_client = MarketApiClient()

    # --- THE MISSING METHOD ---
    async def get_all_market_trends(self) -> Dict[str, Any]:
        """
        Fetches trends for ALL supported crops at once.
        Used by the main Finance Dashboard view.
        """
        market_data = await self.market_client.get_market_prices() # No argument = fetch all
        
        formatted_trends = []
        for crop, data in market_data.items():
            formatted_trends.append({
                "crop": crop.capitalize(),
                "price": f"₹{data.get('current_price', 0)}",
                "unit": "quintal", # Simplified for UI
                "trend": data.get('trend', 'stable')
            })
            
        return {"prices": formatted_trends}

    # --- Single Crop Trend ---
    async def get_market_trends(self, crop: str) -> Dict[str, Any]:
        market_data = await self.market_client.get_market_prices(crop)
        crop_lower = crop.lower()
        
        if crop_lower not in market_data:
             market_data = await self.market_client.get_market_prices()
             
        data = market_data.get(crop_lower, {})
        
        # Simple Prediction Logic
        trend = data.get("trend", "stable")
        multiplier = 1.02 if trend == "rising" else 0.98 if trend == "falling" else 1.0
        predicted = round(data.get("current_price", 0) * multiplier, 2)

        return {
            "crop": crop, 
            "live_price": data.get("current_price"),
            "unit": data.get("unit"),
            "trend": trend, 
            "prediction": {"predicted_price": predicted, "horizon": "7 days", "confidence": "high"},
            "recommendation": "Sell now" if trend == "falling" else "Hold for profit"
        }

    # --- Schemes & Loans (Standard) ---
    def get_schemes_info(self, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        state = user_context.get("state") if user_context else None
        credit = self.crud.get_schemes(db=self.db, data_type="credit", state=state)
        subsidy = self.crud.get_schemes(db=self.db, data_type="subsidy", state=state)

        if not credit and not subsidy:
            live = self._fetch_live_schemes_rss()
            credit = [s for s in live if s['category'] == 'credit']
            subsidy = [s for s in live if s['category'] == 'subsidy']

        return {"credit_schemes": credit, "subsidy_schemes": subsidy, "tips": ["Use KCC for low interest."]}

    def calculate_loan_emi(self, loan_amount: float, repayment_period_months: int, loan_type: str) -> Dict[str, Any]:
        
        # 1. Define Realistic Interest Rates for Indian Agriculture
        # Normalize the input string to handle "Crop Loan" vs "crop loan"
        type_key = loan_type.lower().strip()
        
        rates = {
            "kisan credit card": 7.0,   # Govt Subsidized (KCC)
            "kcc": 7.0,                 # Alias
            "crop loan": 7.0,           # Short term crop loan
            "term loan": 10.0,          # General Term Loan (Pump sets, etc.)
            "tractor loan": 11.0,       # Vehicle/Machinery often higher
            "land development": 9.5     # Land leveling/fencing
        }
        
        # Default to 10.0% if the type is unknown
        annual_rate = rates.get(type_key, 10.0)

        # 2. Calculate EMI (Standard Formula)
        principal = loan_amount
        r = annual_rate / (12 * 100) # Monthly Interest Rate

        if r > 0:
            emi = principal * r * ((1+r)**repayment_period_months) / (((1+r)**repayment_period_months)-1)
        else:
            emi = principal / repayment_period_months

        total_payment = emi * repayment_period_months
        total_interest = total_payment - principal

        # 3. Dynamic Advice based on the specific loan type
        advice = "Standard Rate"
        if annual_rate <= 7.0:
            advice = "Govt Subsidized Rate (Pay on time for extra 3% rebate!)"
        elif annual_rate > 10.5:
            advice = "High Interest Rate - Ensure high ROI from this machinery."

        return {
            "loan_amount": loan_amount, 
            "loan_type": loan_type,            # Echo back the type
            "interest_rate_annual": annual_rate, # The rate used
            "monthly_emi": round(emi, 2), 
            "total_payment": round(total_payment, 2), 
            "total_interest": round(total_interest, 2),
            "advice": advice
        }

    def _fetch_live_schemes_rss(self) -> List[Dict[str, Any]]:
        try:
            feed = feedparser.parse("https://pib.gov.in/RssMain.aspx?ModId=3&LangId=1&Category=6")
            return [{"scheme_name": e.title, "category": "credit" if "loan" in e.title.lower() else "subsidy"} for e in feed.entries[:5]]
        except: return []