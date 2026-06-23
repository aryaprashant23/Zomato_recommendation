"""
Main CLI entry point for the Restaurant Recommender.
"""
import sys
import argparse
import json
from app.config import settings
from app.data.loader import DatasetLoader
from app.data.preprocessor import DataPreprocessor
from app.data.repository import RestaurantRepository
from app.services.groq_client import GroqRecommendationEngine
from app.services.recommendation import RecommendationService
from app.models.preferences import UserPreferences

def main():
    """
    Main entry point function.
    """
    parser = argparse.ArgumentParser(description="AI-Powered Restaurant Recommendation System CLI")
    parser.add_argument("--location", type=str, required=True, help="City or location (e.g., Bangalore)")
    parser.add_argument("--budget", type=str, required=True, choices=["low", "medium", "high"], help="Budget tier")
    parser.add_argument("--cuisine", type=str, default=None, help="Desired cuisine (e.g., Italian)")
    parser.add_argument("--min_rating", type=float, default=0.0, help="Minimum rating (0 to 5)")
    parser.add_argument("--additional", type=str, default=None, help="Additional preferences (e.g., rooftop seating)")
    parser.add_argument("--top_k", type=int, default=settings.TOP_K, help="Number of recommendations")

    args = parser.parse_args()

    print("Loading dataset...")
    try:
        loader = DatasetLoader(settings.DATASET_CACHE_PATH)
        df = loader.load_raw_dataset()
        preprocessor = DataPreprocessor()
        restaurants = preprocessor.preprocess(df)
        repository = RestaurantRepository(restaurants)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    print("Initializing recommendation engine...")
    try:
        engine = GroqRecommendationEngine()
        service = RecommendationService(repository=repository, engine=engine)
    except Exception as e:
        print(f"Error initializing engine: {e}")
        sys.exit(1)

    print("Generating recommendations...\n")
    try:
        prefs = UserPreferences(
            location=args.location,
            budget=args.budget,
            cuisine=args.cuisine,
            min_rating=args.min_rating,
            additional_preferences=args.additional,
            top_k=args.top_k
        )
        result = service.get_recommendations(prefs)
        
        print(f"--- Summary ---")
        print(result["summary"])
        print("\n--- Recommendations ---")
        for rec in result["recommendations"]:
            print(f"#{rec['rank']} - {rec['restaurant_name']}")
            print(f"Cuisine: {rec['cuisine']} | Rating: {rec['rating']} | Cost: {rec['estimated_cost']}")
            print(f"Why: {rec['explanation']}\n")
            
        print(f"Considered {result['meta']['candidates_considered']} candidates in {result['meta']['processing_time_ms']}ms.")
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
