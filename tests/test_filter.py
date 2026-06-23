"""
Unit tests for Phase 2: Preference Filter and Prompt Builder.
"""
import pytest
import json
from app.models.restaurant import Restaurant
from app.models.preferences import UserPreferences
from app.services.filter import PreferenceFilterService
from app.services.prompt import build_recommendation_prompt

# Mock dataset for filtering tests
MOCK_RESTAURANTS = [
    Restaurant(
        id="r1", name="Italian Bistro", location="bangalore", cuisines=["italian", "pizza"],
        rating=4.5, cost_for_two=1200, budget_tier="high", votes=150
    ),
    Restaurant(
        id="r2", name="Pasta Place", location="bangalore", cuisines=["italian", "pasta"],
        rating=4.0, cost_for_two=600, budget_tier="medium", votes=90
    ),
    Restaurant(
        id="r3", name="Pizza Corner", location="bangalore", cuisines=["italian", "pizza"],
        rating=4.0, cost_for_two=300, budget_tier="low", votes=200
    ),
    Restaurant(
        id="r4", name="Delhi Curry House", location="delhi", cuisines=["north indian"],
        rating=4.8, cost_for_two=800, budget_tier="medium", votes=300
    ),
    Restaurant(
        id="r5", name="Bangalore Burger Joint", location="bangalore", cuisines=["fast food", "burger"],
        rating=3.5, cost_for_two=400, budget_tier="low", votes=40
    )
]


def test_filter_by_location():
    # Matches bangalore
    prefs = UserPreferences(
        location="Bangalore", budget="medium", cuisine="Italian", min_rating=3.0, top_k=5
    )
    results = PreferenceFilterService.filter_candidates(MOCK_RESTAURANTS, prefs)
    assert len(results) == 1
    assert results[0].id == "r2"  # "Pasta Place" is Italian, medium budget, in Bangalore


def test_filter_by_cuisine():
    # Matches north indian in delhi
    prefs = UserPreferences(
        location="Delhi", budget="medium", cuisine="North Indian", min_rating=4.0, top_k=5
    )
    results = PreferenceFilterService.filter_candidates(MOCK_RESTAURANTS, prefs)
    assert len(results) == 1
    assert results[0].name == "Delhi Curry House"


def test_filter_rating_threshold():
    # Only return >= 4.2 rating in bangalore
    prefs = UserPreferences(
        location="Bangalore", budget="low", cuisine="Italian", min_rating=4.2, top_k=5
    )
    results = PreferenceFilterService.filter_candidates(MOCK_RESTAURANTS, prefs)
    # Pizza Corner is low budget, Italian in Bangalore but has 4.0 rating (below 4.2)
    assert len(results) == 0


def test_filter_budget_tiers():
    # Low budget Italian in Bangalore
    prefs = UserPreferences(
        location="Bangalore", budget="low", cuisine="Italian", min_rating=3.5, top_k=5
    )
    results = PreferenceFilterService.filter_candidates(MOCK_RESTAURANTS, prefs)
    assert len(results) == 1
    assert results[0].id == "r3"


def test_sorting_order():
    # Multiple matches - sorted by rating desc, then votes desc
    # Add another medium budget Italian in Bangalore to test sorting
    restaurants = MOCK_RESTAURANTS + [
        Restaurant(
            id="r6", name="Toscano", location="bangalore", cuisines=["italian"],
            rating=4.5, cost_for_two=700, budget_tier="medium", votes=50
        ),
        Restaurant(
            id="r7", name="Chianti", location="bangalore", cuisines=["italian"],
            rating=4.5, cost_for_two=800, budget_tier="medium", votes=250
        )
    ]
    prefs = UserPreferences(
        location="Bangalore", budget="medium", cuisine="Italian", min_rating=4.0, top_k=5
    )
    results = PreferenceFilterService.filter_candidates(restaurants, prefs)
    # Toscano (4.5 rating, 50 votes), Chianti (4.5 rating, 250 votes), Pasta Place (4.0 rating, 90 votes)
    # Sort order should be: Chianti (first), Toscano (second), Pasta Place (third)
    assert len(results) == 3
    assert results[0].id == "r7"
    assert results[1].id == "r6"
    assert results[2].id == "r2"


def test_candidate_capping():
    # Create 25 mock candidates matching the preferences
    large_set = []
    for i in range(30):
        large_set.append(Restaurant(
            id=f"idx_{i}", name=f"Rest {i}", location="bangalore", cuisines=["italian"],
            rating=4.0, cost_for_two=600, budget_tier="medium", votes=i
        ))
    prefs = UserPreferences(
        location="Bangalore", budget="medium", cuisine="Italian", min_rating=3.0, top_k=5
    )
    results = PreferenceFilterService.filter_candidates(large_set, prefs, max_candidates=10)
    # Should cap at 10 (overriding default 20 for custom testing)
    assert len(results) == 10
    
    # Default cap testing
    results_default = PreferenceFilterService.filter_candidates(large_set, prefs)
    assert len(results_default) == 20


def test_compact_json_formatting():
    candidates = MOCK_RESTAURANTS[:2]
    json_str = PreferenceFilterService.format_candidates_to_json(candidates)
    parsed = json.loads(json_str)
    
    assert len(parsed) == 2
    assert "approx_cost_for_two" in parsed[0]
    assert "votes" not in parsed[0]  # Excluded fields to save prompt tokens
    assert parsed[0]["name"] == "Italian Bistro"


def test_prompt_builder():
    prefs = UserPreferences(
        location="Delhi", budget="medium", cuisine="North Indian", min_rating=4.0, 
        additional_preferences="family-friendly, quick service", top_k=5
    )
    candidates_json = "[{}]"
    prompt = build_recommendation_prompt(prefs, candidates_json)
    
    assert "Delhi" in prompt
    assert "North Indian" in prompt
    assert "medium" in prompt
    assert "family-friendly, quick service" in prompt
    assert "[{}]" in prompt
