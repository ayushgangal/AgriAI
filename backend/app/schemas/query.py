from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

# Shared properties
class QueryBase(BaseModel):
    query_text: str
    language: Optional[str] = "en"
    response_text: Optional[str] = None
    response_data: Optional[Dict[str, Any]] = None

# Properties to receive on creation
class QueryCreate(QueryBase):
    pass

# Properties to return to client
class Query(QueryBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
