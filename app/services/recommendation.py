from typing import Dict, Any, List
import time
from app.models.preferences import UserPreferences
from app.models.restaurant import Restaurant
from app.data.repository import RestaurantRepository
from app.services.groq_client import GroqRecommendationEngine
from app.services.filter import PreferenceFilterService


class RecommendationService:
    """
    Coordinates data ingestion outputs, filtering logic, and LLM requests
    to generate end-to-end user recommendation results.
    """
    def __init__(self, repository: RestaurantRepository, engine: GroqRecommendationEngine):
        self.repository = repository
        self.engine = engine

    def get_recommendations(self, preferences: UserPreferences) -> Dict[str, Any]:
        """
        Runs recommendation workflow.
        """
        start_time = time.time()
        
        # 1. Get all candidates
        all_restaurants = self.repository.get_all()
        
        # 2. Filter down to candidates matching preferences
        filtered_candidates = PreferenceFilterService.filter_candidates(
            restaurants=all_restaurants,
            preferences=preferences
        )
        
        if not filtered_candidates:
            return {
                "summary": "No restaurants match your criteria. Try broadening location, cuisine, or rating.",
                "recommendations": [],
                "meta": {
                    "candidates_considered": 0,
                    "processing_time_ms": int((time.time() - start_time) * 1000)
                }
            }
            
        # 3. Call Groq
        response = self.engine.get_recommendations(preferences, filtered_candidates)
        
        # 4. Format output
        recommendations = []
        for rec in response.recommendations:
            recommendations.append({
                "rank": rec.rank,
                "restaurant_name": rec.restaurant.name,
                "cuisine": ", ".join(rec.restaurant.cuisines),
                "rating": rec.restaurant.rating,
                "estimated_cost": f"Rs. {rec.restaurant.cost_for_two}" if rec.restaurant.cost_for_two else "unknown",
                "explanation": rec.explanation
            })
            
        return {
            "summary": response.summary,
            "recommendations": recommendations,
            "meta": {
                "candidates_considered": len(filtered_candidates),
                "processing_time_ms": int((time.time() - start_time) * 1000)
            }
        }
