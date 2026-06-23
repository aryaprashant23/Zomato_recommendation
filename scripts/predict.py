import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from app.models.preferences import UserPreferences
from app.models.restaurant import Restaurant
from app.data.loader import DatasetLoader
from app.data.preprocessor import DataPreprocessor
from app.data.repository import RestaurantRepository
from app.services.groq_client import GroqRecommendationEngine
from app.services.recommendation import RecommendationService

def main():
    print("Loading data... (this might take a moment if not cached)")
    try:
        loader = DatasetLoader(cache_path=settings.DATASET_CACHE_PATH)
        raw_df = loader.load_raw_dataset()
        preprocessor = DataPreprocessor()
        restaurants = preprocessor.preprocess(raw_df)
    except Exception as e:
        print(f"Warning: Could not load real dataset ({e}). Falling back to dummy data for demonstration.")
        restaurants = [
            Restaurant(
                id="r1",
                name="Bellandur Royal Dine",
                location="bellandur",
                cuisines=["north indian", "chinese"],
                rating=4.6,
                cost_for_two=1400,
                budget_tier="high",
                votes=1200
            ),
            Restaurant(
                id="r2",
                name="Pasta Street Bellandur",
                location="bellandur",
                cuisines=["italian"],
                rating=4.5,
                cost_for_two=1600,
                budget_tier="high",
                votes=800
            ),
            Restaurant(
                id="r3",
                name="Cheap Eats",
                location="bellandur",
                cuisines=["south indian"],
                rating=3.5,
                cost_for_two=400,
                budget_tier="low",
                votes=150
            )
        ]
    
    repo = RestaurantRepository(restaurants=restaurants)
    engine = GroqRecommendationEngine()
    service = RecommendationService(repo, engine)

    # User inputs: Location: Balendur ; Budget: 1500; Rating: 4.5
    prefs = UserPreferences(
        location="bellandur", 
        budget="high", 
        min_rating=4.5,
        cuisine=None, 
        top_k=5
    )

    print(f"Requesting top {prefs.top_k} restaurants for location: {prefs.location}, budget: {prefs.budget}, min rating: {prefs.min_rating}")
    
    results = service.get_recommendations(prefs)
    
    print("\n=== SUMMARY ===")
    print(results.get("summary", "No summary available"))
    print("\n=== RECOMMENDATIONS ===")
    
    recs = results.get("recommendations", [])
    if not recs:
        print("No recommendations found.")
    
    for rec in recs:
        print(f"{rec['rank']}. {rec['restaurant_name']} (Rating: {rec['rating']}, Cost: {rec['estimated_cost']})")
        print(f"   Cuisine: {rec['cuisine']}")
        print(f"   Why: {rec['explanation']}\n")
        
    print(f"Meta: {json.dumps(results.get('meta', {}))}")

if __name__ == "__main__":
    main()
