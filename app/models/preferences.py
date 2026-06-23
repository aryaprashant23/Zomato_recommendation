"""
User preference models for validating filtering inputs.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class UserPreferences(BaseModel):
    """
    Structured model for user recommendation preferences.
    """
    location: str = Field(..., min_length=1, description="Normalized location / city name")
    budget: str = Field(..., description="Desired budget tier (low, medium, high)")
    cuisine: Optional[str] = Field(None, description="Desired cuisine tag, or None for any")
    min_rating: float = Field(default=0.0, ge=0.0, le=5.0, description="Minimum numeric rating threshold (0.0 to 5.0)")
    additional_preferences: Optional[str] = Field(None, max_length=150, description="Free-text additional preferences")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of recommendations to return")

    @field_validator("budget")
    @classmethod
    def validate_budget_tier(cls, v: str) -> str:
        """Validate budget tier value."""
        lower_v = v.lower()
        if lower_v not in {"low", "medium", "high"}:
            raise ValueError("Budget tier must be one of: low, medium, high")
        return lower_v
