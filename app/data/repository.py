"""
Data repository acting as an in-memory database wrapper for normalized restaurants.
"""
from typing import List, Set
from app.models.restaurant import Restaurant


class RestaurantRepository:
    """
    Manages in-memory list of restaurants, providing helper queries for filtering,
    locations, and cuisines list.
    """
    def __init__(self, restaurants: List[Restaurant]):
        self._restaurants = restaurants
        # Extract unique sorted locations
        self._locations = sorted(list({r.location for r in restaurants if r.location}))
        # Extract unique sorted cuisines
        all_cuisines = set()
        for r in restaurants:
            for cuisine in r.cuisines:
                if cuisine:
                    all_cuisines.add(cuisine)
        self._cuisines = sorted(list(all_cuisines))

    def get_all(self) -> List[Restaurant]:
        """Return all restaurants in repository."""
        return self._restaurants

    def get_locations(self) -> List[str]:
        """Return list of distinct normalized locations."""
        return self._locations

    def get_cuisines(self) -> List[str]:
        """Return list of distinct normalized cuisines."""
        return self._cuisines

