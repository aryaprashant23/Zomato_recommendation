"""
HTTP endpoints for web service consumption of the recommendation engine.
"""
from fastapi import APIRouter, Request, HTTPException
from app.models.preferences import UserPreferences
from app.config import settings

router = APIRouter()

@router.get("/health")
def health_check(request: Request):
    """Returns database readiness and API config connectivity status."""
    repo = getattr(request.app.state, "repository", None)
    service = getattr(request.app.state, "recommendation_service", None)
    return {
        "status": "ok", 
        "message": "API is up and running.",
        "dataset_loaded": repo is not None,
        "service_ready": service is not None,
        "groq_configured": bool(settings.GROQ_API_KEY)
    }

@router.get("/locations")
def get_locations(request: Request):
    """Returns a list of distinct cities/locations available in the dataset."""
    repo = getattr(request.app.state, "repository", None)
    if not repo:
        raise HTTPException(status_code=503, detail="Data repository not initialized")
    return repo.get_locations()

@router.get("/cuisines")
def get_cuisines(request: Request):
    """Returns a list of distinct cuisines available in the dataset."""
    repo = getattr(request.app.state, "repository", None)
    if not repo:
        raise HTTPException(status_code=503, detail="Data repository not initialized")
    return repo.get_cuisines()

@router.post("/recommend")
def recommend_restaurants(preferences: UserPreferences, request: Request):
    """Generates restaurant recommendations based on user preferences."""
    service = getattr(request.app.state, "recommendation_service", None)
    if not service:
        raise HTTPException(status_code=503, detail="Recommendation service not initialized")
    
    try:
        # The preference validation is automatically handled by FastAPI + Pydantic
        result = service.get_recommendations(preferences)
        return result
    except Exception as e:
        # Fallback error handling
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")
