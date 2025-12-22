from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100))
    phone_number = Column(String(15))
    # Hashed password for authentication
    hashed_password = Column(String(128))
    
    # Location information
    state = Column(String(50))
    district = Column(String(50))
    village = Column(String(100))
    latitude = Column(String(20))
    longitude = Column(String(20))
    
    # Preferences
    preferred_language = Column(String(10), default="en")
    preferred_crops = Column(Text)  # JSON string of crop preferences
    farm_size = Column(String(50))  # in acres/hectares
    irrigation_type = Column(String(50))  # drip, sprinkler, flood, etc.
    
    # Settings
    notifications_enabled = Column(Boolean, default=True)
    offline_mode_enabled = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    queries = relationship("Query", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>" 