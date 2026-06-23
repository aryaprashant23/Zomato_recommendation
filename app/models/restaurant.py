"""
Restaurant models representing canonical restaurant fields parsed from the dataset.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class Restaurant(BaseModel):
    """
    Canonical data model for a single restaurant.
    """
    id: str = Field(..., description="Stable identifier generated from name and location")
    name: str = Field(..., description="Name of the restaurant")
    location: str = Field(..., description="Normalized city or area")
    cuisines: List[str] = Field(default_factory=list, description="List of cuisine tags")
    rating: float = Field(default=0.0, description="Normalized rating on a 0-5 scale")
    cost_for_two: Optional[int] = Field(None, description="Average cost for two people")
    budget_tier: str = Field(..., description="Calculated budget tier (low, medium, high)")
    address: Optional[str] = Field(None, description="Physical address of the restaurant")
    rest_type: Optional[str] = Field(None, description="Restaurant type (e.g. Cafe, Casual Dining)")
    online_order: Optional[bool] = Field(None, description="Availability of online ordering")
    book_table: Optional[bool] = Field(None, description="Availability of table booking")
    votes: int = Field(default=0, description="Number of user ratings or votes")
