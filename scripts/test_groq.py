import os
import sys
from pathlib import Path

# Add the project root to the python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.preferences import UserPreferences
from app.models.restaurant import Restaurant
from app.services.groq_client import GroqRecommendationEngine

def main():
    print("Testing GroqRecommendationEngine...")
    engine = GroqRecommendationEngine()
    
    # Create sample preferences
    prefs = UserPreferences(
        location="bangalore",
        budget="medium",
        cuisine="italian",
        min_rating=4.0,
        top_k=2
    )
    
    # Create sample candidates
    candidates = [
        Restaurant(
            id="r1",
            name="Pizza Bakery",
            location="bangalore",
            cuisines=["italian", "pizza"],
            rating=4.6,
            cost_for_two=1200,
            budget_tier="medium",
            votes=500
        ),
        Restaurant(
            id="r2",
            name="Pasta Street",
            location="bangalore",
            cuisines=["italian"],
            rating=4.2,
            cost_for_two=900,
            budget_tier="medium",
            votes=300
        ),
        Restaurant(
            id="r3",
            name="Cheap Eats",
            location="bangalore",
            cuisines=["italian"],
            rating=3.5,
            cost_for_two=400,
            budget_tier="low",
            votes=150
        )
    ]
    
    print("\nCalling Groq...")
    response = engine.get_recommendations(prefs, candidates)
    
    print("\n=== RESULTS ===")
    print(f"Summary: {response.summary}\n")
    for rec in response.recommendations:
        print(f"Rank {rec.rank}: {rec.restaurant.name} (Rating: {rec.restaurant.rating})")
        print(f"Explanation: {rec.explanation}")
        print("-" * 20)

if __name__ == "__main__":
    main()
