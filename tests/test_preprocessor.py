import pandas as pd
import pytest
from app.data.preprocessor import DataPreprocessor
from app.models.restaurant import Restaurant


def test_preprocessor_rating_parsing():
    preprocessor = DataPreprocessor()
    assert preprocessor._parse_rating("4.1/5") == 4.1
    assert preprocessor._parse_rating("3.8 /5") == 3.8
    assert preprocessor._parse_rating("NEW") == 0.0
    assert preprocessor._parse_rating("-") == 0.0
    assert preprocessor._parse_rating("4.5") == 4.5
    assert preprocessor._parse_rating(None) == 0.0


def test_preprocessor_cost_parsing():
    preprocessor = DataPreprocessor()
    assert preprocessor._parse_cost("1,200") == 1200
    assert preprocessor._parse_cost("₹ 500") == 500
    assert preprocessor._parse_cost("NaN") is None
    assert preprocessor._parse_cost(None) is None


def test_preprocessor_location_normalization():
    preprocessor = DataPreprocessor()
    assert preprocessor._normalize_location("Bengaluru ") == "bangalore"
    assert preprocessor._normalize_location("New Delhi") == "delhi"
    assert preprocessor._normalize_location("unknown") == "unknown"


def test_preprocessor_cuisine_parsing():
    preprocessor = DataPreprocessor()
    assert preprocessor._parse_cuisines("Italian, Chinese") == ["italian", "chinese"]
    assert preprocessor._parse_cuisines("Italian ,Chinese") == ["italian", "chinese"]
    assert preprocessor._parse_cuisines(None) == []


def test_preprocessor_full_pipeline():
    # Mock dataframe with raw dataset variations
    raw_data = {
        "name": ["Rest A", "Rest A", "Rest B", "Rest C"],
        "location": ["Bengaluru", "Bangalore", "Delhi", "Mumbai"],
        "cuisines": ["Italian, Chinese", "Italian", "North Indian", "Fast Food"],
        "rate": ["4.5/5", "4.0/5", "NEW", "3.8"],
        "approx_cost(for two people)": ["1,200", "1,000", "300", "600"],
        "address": ["Address A", "Address A2", "Address B", "Address C"],
        "rest_type": ["Cafe", "Cafe", "Quick Bites", "Dine-out"],
        "online_order": ["Yes", "No", "Yes", "No"],
        "book_table": ["Yes", "No", "No", "No"],
        "votes": [100, 50, 0, 10]
    }
    df = pd.DataFrame(raw_data)
    preprocessor = DataPreprocessor()
    cleaned = preprocessor.preprocess(df)
    
    # 4 rows originally, but "Rest A" has a duplicate (same name + location)
    # Deduplication should keep the one with higher rating/votes (Rest A with 4.5 rating)
    assert len(cleaned) == 3
    
    # Verify deduplication details
    rest_a = next(r for r in cleaned if r.name == "Rest A")
    assert rest_a.rating == 4.5
    assert rest_a.location == "bangalore"
    assert rest_a.cuisines == ["italian", "chinese"]
    assert rest_a.votes == 100
    assert rest_a.cost_for_two == 1200
    assert rest_a.online_order is True
    
    # Check budget tiers computed from percentiles of costs
    for r in cleaned:
        assert r.budget_tier in ("low", "medium", "high")

