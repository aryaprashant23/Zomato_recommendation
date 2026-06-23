import json
from typing import List
from app.models.restaurant import Restaurant
from app.models.preferences import UserPreferences
from app.config import settings


class PreferenceFilterService:
    """
    Applies logic to filter down in-memory list to candidates matching location, cuisine,
    rating, and budget constraints.
    """
    @staticmethod
    def filter_candidates(
        restaurants: List[Restaurant], 
        preferences: UserPreferences, 
        max_candidates: int = None
    ) -> List[Restaurant]:
        """
        Filters candidates based on preferences and sorts by rating.
        Caps candidates list to MAX_CANDIDATES threshold.
        """
        if max_candidates is None:
            max_candidates = settings.MAX_CANDIDATES

        loc_query = preferences.location.strip().lower()
        cuisine_query = preferences.cuisine.strip().lower() if preferences.cuisine else None
        budget_query = preferences.budget.strip().lower()
        min_rating_query = preferences.min_rating

        filtered = []
        for r in restaurants:
            # 1. Location match
            if r.location.strip().lower() != loc_query:
                continue

            # 2. Cuisine match (search query tag inside the cuisines list)
            if cuisine_query and cuisine_query not in [c.strip().lower() for c in r.cuisines]:
                continue

            # 3. Rating threshold check
            if r.rating < min_rating_query:
                continue

            # 4. Budget tier match
            if r.budget_tier.strip().lower() != budget_query:
                continue

            filtered.append(r)

        # Sort by rating desc, then votes desc
        filtered.sort(key=lambda r: (r.rating, r.votes), reverse=True)

        return filtered[:max_candidates]

    @staticmethod
    def format_candidates_to_json(candidates: List[Restaurant]) -> str:
        """
        Serializes candidates list to a compact JSON string.
        Optimized to exclude redundant columns to conserve prompt token usage.
        """
        compact_data = []
        for c in candidates:
            compact_data.append({
                "id": c.id,
                "name": c.name,
                "cuisines": c.cuisines,
                "rating": c.rating,
                "approx_cost_for_two": f"Rs. {c.cost_for_two}" if c.cost_for_two else "unknown",
                "budget_tier": c.budget_tier,
                "location": c.location,
                "rest_type": c.rest_type or "unknown"
            })
        return json.dumps(compact_data, indent=2)

