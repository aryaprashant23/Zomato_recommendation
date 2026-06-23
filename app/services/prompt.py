"""
Prompt builder module to construct structured templates for Groq API consumption.
"""
from pathlib import Path
from app.models.preferences import UserPreferences
from app.config import settings

TEMPLATE_PATH = settings.BASE_DIR / "prompts" / "recommendation.txt"


def build_recommendation_prompt(preferences: UserPreferences, candidates_json: str) -> str:
    """
    Loads the prompt template and injects preferences and serialized candidates.
    """
    # Fallback default template if file cannot be read
    default_template = (
        "Rank the following restaurants based on user preferences:\n"
        "Location: {location}\n"
        "Budget: {budget}\n"
        "Cuisine: {cuisine}\n"
        "Min Rating: {min_rating}\n"
        "Additional Notes: {additional_preferences}\n\n"
        "Candidates:\n{candidates_json}\n\n"
        "Return output as a valid JSON object matching this schema:\n"
        "{{\n"
        "  \"summary\": \"Overall summary of choices\",\n"
        "  \"recommendations\": [\n"
        "    {{\n"
        "      \"restaurant_id\": \"id\",\n"
        "      \"rank\": 1,\n"
        "      \"explanation\": \"1-2 sentences reason\"\n"
        "    }}\n"
        "  ]\n"
        "}}"
    )

    template = default_template
    if TEMPLATE_PATH.exists():
        try:
            with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
                template = f.read()
        except Exception:
            # Fall back to inline default if reading fails
            pass

    # Sanitize user preferences string injection for prompt safety
    sanitized_additional = (
        preferences.additional_preferences.replace("{", "{{").replace("}", "}}")
        if preferences.additional_preferences
        else "None"
    )

    formatted_prompt = template.format(
        location=preferences.location,
        budget=preferences.budget,
        cuisine=preferences.cuisine,
        min_rating=preferences.min_rating,
        additional_preferences=sanitized_additional,
        candidates_json=candidates_json,
        top_k=preferences.top_k
    )

    return formatted_prompt
