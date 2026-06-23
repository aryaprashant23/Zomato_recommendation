import json
import pytest
from app.models.restaurant import Restaurant
from app.models.preferences import UserPreferences
from app.services.groq_client import GroqRecommendationEngine

@pytest.fixture
def sample_candidates():
    return [
        Restaurant(
            id="r1",
            name="Pizza Palace",
            location="bangalore",
            cuisines=["italian", "pizza"],
            rating=4.5,
            cost_for_two=800,
            budget_tier="medium",
            votes=100
        ),
        Restaurant(
            id="r2",
            name="Burger Joint",
            location="bangalore",
            cuisines=["american", "burger"],
            rating=4.0,
            cost_for_two=500,
            budget_tier="low",
            votes=50
        )
    ]

@pytest.fixture
def preferences():
    return UserPreferences(
        location="bangalore",
        budget="medium",
        cuisine="italian",
        min_rating=4.0,
        top_k=2
    )

def test_parse_valid_json(sample_candidates):
    engine = GroqRecommendationEngine(api_key="dummy")
    
    valid_json = json.dumps({
        "summary": "Here are some great options.",
        "recommendations": [
            {
                "restaurant_id": "r1",
                "rank": 1,
                "explanation": "Great pizza."
            },
            {
                "restaurant_id": "r2",
                "rank": 2,
                "explanation": "Good burgers."
            }
        ]
    })
    
    result = engine._parse_response(valid_json, sample_candidates, k=2)
    assert result.summary == "Here are some great options."
    assert len(result.recommendations) == 2
    assert result.recommendations[0].restaurant.id == "r1"
    assert result.recommendations[0].rank == 1
    assert result.recommendations[1].restaurant.id == "r2"

def test_hallucinated_id_rejection(sample_candidates):
    engine = GroqRecommendationEngine(api_key="dummy")
    
    json_with_hallucination = json.dumps({
        "summary": "Summary",
        "recommendations": [
            {
                "restaurant_id": "r1",
                "rank": 1,
                "explanation": "Real"
            },
            {
                "restaurant_id": "fake_id",
                "rank": 2,
                "explanation": "Fake"
            }
        ]
    })
    
    result = engine._parse_response(json_with_hallucination, sample_candidates, k=2)
    assert len(result.recommendations) == 1
    assert result.recommendations[0].restaurant.id == "r1"

def test_fallback_recommendations(sample_candidates, preferences):
    engine = GroqRecommendationEngine(api_key="dummy")
    result = engine._fallback_recommendations(sample_candidates, k=2)
    
    assert len(result.recommendations) == 2
    # Should be sorted by rating desc
    assert result.recommendations[0].restaurant.id == "r1"
    assert result.recommendations[1].restaurant.id == "r2"
    assert result.summary.startswith("We experienced an issue")

def test_invalid_json_handling(sample_candidates):
    engine = GroqRecommendationEngine(api_key="dummy")
    with pytest.raises(json.JSONDecodeError):
        engine._parse_response("not json", sample_candidates, k=2)
