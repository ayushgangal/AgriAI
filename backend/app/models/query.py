from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Query(Base):
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Query information
    query_text = Column(Text, nullable=False)
    query_type = Column(String(50))  # weather, crop, finance, irrigation, etc.
    query_language = Column(String(10), default="en")
    
    # Input modalities
    input_type = Column(String(20), default="text")  # text, voice, image
    input_data = Column(JSON)  # Store additional input data (voice file, image, etc.)
    
    # AI response
    response_text = Column(Text, nullable=False)
    response_data = Column(JSON)  # Structured response data
    confidence_score = Column(String(10))  # AI confidence in response
    
    # Context information
    location = Column(String(100))
    weather_conditions = Column(JSON)  # Weather data at time of query
    crop_context = Column(JSON)  # Current crop information
    
    # Metadata
    processing_time = Column(String(20))  # Time taken to process query
    model_used = Column(String(50))  # Which AI model was used
    data_sources = Column(JSON)  # Sources used for response
    
    # User feedback
    user_rating = Column(Integer)  # 1-5 rating
    user_feedback = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="queries")
    
    def __repr__(self):
        return f"<Query(id={self.id}, type='{self.query_type}', text='{self.query_text[:50]}...')>" 