import hashlib
import re
from typing import List, Optional, Any
import numpy as np
import pandas as pd
from app.models.restaurant import Restaurant

LOCATION_ALIASES = {
    "bengaluru": "bangalore",
    "new delhi": "delhi",
    "delhi ncr": "delhi",
}


class DataPreprocessor:
    """
    Cleans raw pandas columns and transforms them into unified Restaurant schema structures.
    """
    def __init__(self):
        # Mapping to check for column name variations in the source dataset
        self.column_mapping = {
            "name": ["name", "Name", "restaurant_name"],
            "location": ["location", "Location", "city", "listed_in(city)"],
            "cuisines": ["cuisines", "Cuisines", "cuisine", "Cuisine"],
            "rate": ["rate", "Rate", "rating", "Rating", "restaurant_rating"],
            "approx_cost": [
                "approx_cost(for two people)",
                "approx_cost_for_two_people",
                "approx_cost",
                "cost",
                "Cost",
                "cost_for_two"
            ],
            "address": ["address", "Address"],
            "rest_type": ["rest_type", "Rest Type", "restaurant_type", "type"],
            "online_order": ["online_order", "Online Order", "online"],
            "book_table": ["book_table", "Book Table", "booking"],
            "votes": ["votes", "Votes", "vote_count"]
        }

    def _find_column(self, df: pd.DataFrame, key: str) -> Optional[str]:
        """Finds the actual column name in DataFrame matching any of the aliases."""
        for alias in self.column_mapping.get(key, []):
            if alias in df.columns:
                return alias
        return None

    def _normalize_location(self, loc: Any) -> str:
        """Trims, lowercases, and maps location to standard alias."""
        if pd.isna(loc) or not isinstance(loc, str):
            return "unknown"
        cleaned = loc.strip().lower()
        return LOCATION_ALIASES.get(cleaned, cleaned)

    def _parse_cuisines(self, cuisine_val: Any) -> List[str]:
        """Splits comma-separated cuisine string into list of stripped tags."""
        if pd.isna(cuisine_val) or not isinstance(cuisine_val, str):
            return []
        # Split by comma or semicolon, trim, and lowercase
        tags = [c.strip().lower() for c in re.split(r"[,;]+", cuisine_val) if c.strip()]
        return tags

    def _parse_rating(self, rate_val: Any) -> float:
        """Coerces ratings to float between 0.0 and 5.0, handling 'NEW', '-', etc."""
        if pd.isna(rate_val):
            return 0.0
        
        rate_str = str(rate_val).strip()
        if rate_str.upper() in ("NEW", "-", ""):
            return 0.0

        # Try to extract the score (e.g. 4.1/5 or 4.1 /5 or just 4.1)
        match = re.match(r"^([0-9.]+)\s*/\s*5", rate_str)
        if match:
            try:
                val = float(match.group(1))
                return min(max(val, 0.0), 5.0)
            except ValueError:
                pass
        
        # Try raw float parsing
        try:
            val = float(rate_str)
            return min(max(val, 0.0), 5.0)
        except ValueError:
            pass

        return 0.0

    def _parse_cost(self, cost_val: Any) -> Optional[int]:
        """Strips currency symbols/commas and returns cost as integer."""
        if pd.isna(cost_val):
            return None
        cost_str = str(cost_val).strip()
        # Remove commas, currency symbols, and spaces
        cleaned = re.sub(r"[^\d]", "", cost_str)
        if cleaned:
            try:
                return int(cleaned)
            except ValueError:
                pass
        return None

    def _parse_bool(self, val: Any) -> Optional[bool]:
        """Parses Yes/No/True/False/1/0 into boolean."""
        if pd.isna(val):
            return None
        if isinstance(val, bool):
            return val
        val_str = str(val).strip().lower()
        if val_str in ("yes", "true", "1"):
            return True
        if val_str in ("no", "false", "0"):
            return False
        return None

    def preprocess(self, df: pd.DataFrame) -> List[Restaurant]:
        """
        Processes pandas DataFrame columns and parses into Restaurant pydantic objects.
        
        Args:
            df (pd.DataFrame): Raw restaurant data.
            
        Returns:
            List[Restaurant]: List of structured restaurant objects.
        """
        # Find matching column names
        col_name = self._find_column(df, "name") or "name"
        col_loc = self._find_column(df, "location") or "location"
        col_cuisines = self._find_column(df, "cuisines") or "cuisines"
        col_rate = self._find_column(df, "rate") or "rate"
        col_cost = self._find_column(df, "approx_cost") or "approx_cost"
        col_address = self._find_column(df, "address") or "address"
        col_rest_type = self._find_column(df, "rest_type") or "rest_type"
        col_online = self._find_column(df, "online_order") or "online_order"
        col_book = self._find_column(df, "book_table") or "book_table"
        col_votes = self._find_column(df, "votes") or "votes"

        temp_list = []
        
        # Determine budget tier boundaries based on percentiles of non-null cost values
        all_costs = []
        if col_cost in df.columns:
            for cost_val in df[col_cost]:
                parsed_c = self._parse_cost(cost_val)
                if parsed_c is not None:
                    all_costs.append(parsed_c)
        
        p33 = 400  # Default fallback thresholds if no data exists
        p66 = 800
        if all_costs:
            p33 = np.percentile(all_costs, 33)
            p66 = np.percentile(all_costs, 66)

        for _, row in df.iterrows():
            # Get values safely
            raw_name = str(row.get(col_name, "Unknown")).strip()
            raw_loc = row.get(col_loc, "unknown")
            raw_cuisines = row.get(col_cuisines, "")
            raw_rate = row.get(col_rate, 0.0)
            raw_cost = row.get(col_cost, None)
            raw_address = row.get(col_address, None)
            raw_rest_type = row.get(col_rest_type, None)
            raw_online = row.get(col_online, None)
            raw_book = row.get(col_book, None)
            raw_votes = row.get(col_votes, 0)

            # Clean and normalize
            normalized_name = raw_name
            normalized_loc = self._normalize_location(raw_loc)
            parsed_cuisines_list = self._parse_cuisines(raw_cuisines)
            parsed_rate = self._parse_rating(raw_rate)
            parsed_cost = self._parse_cost(raw_cost)

            # Determine budget tier
            if parsed_cost is None:
                budget_tier = "medium"  # Fallback tier
            elif parsed_cost <= p33:
                budget_tier = "low"
            elif parsed_cost <= p66:
                budget_tier = "medium"
            else:
                budget_tier = "high"

            # Parse optional fields
            address_val = str(raw_address).strip() if pd.notna(raw_address) else None
            rest_type_val = str(raw_rest_type).strip() if pd.notna(raw_rest_type) else None
            online_val = self._parse_bool(raw_online)
            book_val = self._parse_bool(raw_book)
            
            try:
                votes_val = int(raw_votes)
            except (ValueError, TypeError):
                votes_val = 0

            # Generate stable ID
            id_input = f"{normalized_name.lower()}::{normalized_loc}"
            stable_id = hashlib.md5(id_input.encode("utf-8")).hexdigest()

            # Create restaurant dict for deduplication sorting
            temp_list.append({
                "id": stable_id,
                "name": normalized_name,
                "location": normalized_loc,
                "cuisines": parsed_cuisines_list,
                "rating": parsed_rate,
                "cost_for_two": parsed_cost,
                "budget_tier": budget_tier,
                "address": address_val,
                "rest_type": rest_type_val,
                "online_order": online_val,
                "book_table": book_val,
                "votes": votes_val
            })

        # Convert to DataFrame to deduplicate by name + location
        # If duplicates exist, sort by rating and votes descending so we keep the best rated/voted entry
        temp_df = pd.DataFrame(temp_list)
        if temp_df.empty:
            return []

        temp_df = temp_df.sort_values(by=["rating", "votes"], ascending=False)
        temp_df = temp_df.drop_duplicates(subset=["name", "location"], keep="first")

        # Convert back to List of Restaurant models
        cleaned_restaurants = []
        for _, row in temp_df.iterrows():
            restaurant = Restaurant(
                id=row["id"],
                name=row["name"],
                location=row["location"],
                cuisines=row["cuisines"],
                rating=row["rating"],
                cost_for_two=row["cost_for_two"] if pd.notna(row["cost_for_two"]) else None,
                budget_tier=row["budget_tier"],
                address=row["address"] if pd.notna(row["address"]) else None,
                rest_type=row["rest_type"] if pd.notna(row["rest_type"]) else None,
                online_order=row["online_order"] if pd.notna(row["online_order"]) else None,
                book_table=row["book_table"] if pd.notna(row["book_table"]) else None,
                votes=int(row["votes"])
            )
            cleaned_restaurants.append(restaurant)

        return cleaned_restaurants

