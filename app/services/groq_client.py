import json
import logging
from typing import List, Dict, Any

from groq import Groq

from app.config import settings
from app.models.restaurant import Restaurant
from app.models.preferences import UserPreferences
from app.models.recommendation import RecommendationResponse, RecommendedRestaurant
from app.services.filter import PreferenceFilterService

logger = logging.getLogger(__name__)

class GroqRecommendationEngine:
    """
    Constructs prompts, requests Groq API chat completions, parses responses,
    and handles JSON parser issues.
    """
    def __init__(self, api_key: str = None, model: str = None, temperature: float = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL
        self.temperature = temperature if temperature is not None else settings.GROQ_TEMPERATURE
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        
    def _build_prompt(self, preferences: UserPreferences, candidates: List[Restaurant]) -> str:
        prompt_path = settings.BASE_DIR / "prompts" / "recommendation.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
            
        candidates_json = PreferenceFilterService.format_candidates_to_json(candidates)
        
        return template.format(
            location=preferences.location,
            budget=preferences.budget,
            cuisine=preferences.cuisine,
            min_rating=preferences.min_rating,
            additional_preferences=preferences.additional_preferences or "None",
            top_k=preferences.top_k,
            candidates_json=candidates_json
        )
        
    def get_recommendations(self, preferences: UserPreferences, candidates: List[Restaurant]) -> RecommendationResponse:
        """
        Sends candidates to Groq, ranks them, and obtains reasoning descriptions.
        """
        if not candidates:
            return RecommendationResponse(summary="No candidates available.", recommendations=[])
            
        k = min(preferences.top_k, len(candidates))
        preferences.top_k = k
        
        if not self.client:
            logger.warning("Groq API key not set. Falling back to rating-sorted results.")
            return self._fallback_recommendations(candidates, k)
            
        prompt = self._build_prompt(preferences, candidates)
        
        try:
            return self._call_groq_and_parse(prompt, candidates, k, retry=True)
        except Exception as e:
            logger.error(f"Groq API error or parse failure: {e}")
            return self._fallback_recommendations(candidates, k)
            
    def _call_groq_and_parse(self, prompt: str, candidates: List[Restaurant], k: int, retry: bool = True) -> RecommendationResponse:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a personalized restaurant recommendation assistant. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=self.temperature,
                timeout=15.0
            )
            
            content = response.choices[0].message.content
            return self._parse_response(content, candidates, k)
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse Groq response: {e}")
            if retry:
                logger.info("Retrying with stricter JSON instructions.")
                stricter_prompt = prompt + "\n\nIMPORTANT: You MUST return strictly valid JSON matching the requested format. Do not include markdown formatting or extra text."
                return self._call_groq_and_parse(stricter_prompt, candidates, k, retry=False)
            raise e
            
    def _parse_response(self, content: str, candidates: List[Restaurant], k: int) -> RecommendationResponse:
        data = json.loads(content)
        
        summary = data.get("summary")
        recs_data = data.get("recommendations", [])
        
        if not isinstance(recs_data, list):
            raise ValueError("Recommendations must be a list")
            
        candidate_map = {c.id: c for c in candidates}
        
        valid_recs = []
        seen_ranks = set()
        
        for item in recs_data:
            r_id = item.get("restaurant_id")
            rank = item.get("rank")
            explanation = item.get("explanation", "Highly recommended based on your preferences.")
            
            if r_id not in candidate_map:
                continue 
                
            if rank in seen_ranks or not isinstance(rank, int):
                rank = max(seen_ranks) + 1 if seen_ranks else 1
                
            seen_ranks.add(rank)
            
            valid_recs.append({
                "restaurant": candidate_map[r_id],
                "rank": rank,
                "explanation": explanation
            })
            
        valid_recs.sort(key=lambda x: x["rank"])
        
        final_recs = []
        for i, rec in enumerate(valid_recs[:k]):
            final_recs.append(
                RecommendedRestaurant(
                    restaurant=rec["restaurant"],
                    rank=i + 1,
                    explanation=rec["explanation"]
                )
            )
            
        if not final_recs:
            raise ValueError("No valid recommendations parsed from Groq response")
            
        return RecommendationResponse(
            summary=summary,
            recommendations=final_recs
        )
        
    def _fallback_recommendations(self, candidates: List[Restaurant], k: int) -> RecommendationResponse:
        sorted_candidates = sorted(candidates, key=lambda x: (x.rating, x.votes), reverse=True)
        top_candidates = sorted_candidates[:k]
        
        recs = []
        for i, c in enumerate(top_candidates):
            recs.append(
                RecommendedRestaurant(
                    restaurant=c,
                    rank=i + 1,
                    explanation=f"A highly-rated {c.budget_tier} budget option offering {', '.join(c.cuisines)}."
                )
            )
            
        return RecommendationResponse(
            summary="We experienced an issue generating personalized recommendations, but here are the top-rated matches for your criteria.",
            recommendations=recs
        )
