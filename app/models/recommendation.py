from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.restaurant import Restaurant

class RecommendedRestaurant(BaseModel):
    restaurant: Restaurant
    rank: int
    explanation: str

class RecommendationResponse(BaseModel):
    summary: Optional[str] = None
    recommendations: List[RecommendedRestaurant]
