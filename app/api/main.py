"""
FastAPI application entry point.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys

from app.api.routes import router
from app.config import settings
from app.data.repository import RestaurantRepository
from app.services.groq_client import GroqRecommendationEngine
from app.services.recommendation import RecommendationService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load dataset and initialize services
    try:
        print("Loading preprocessed dataset for API...")
        import json
        from pathlib import Path
        
        data_path = Path("data/restaurants_processed.json")
        if data_path.exists():
            with open(data_path, "r", encoding="utf-8") as f:
                restaurants_data = json.load(f)
            from app.models.restaurant import Restaurant
            restaurants = [Restaurant(**r) for r in restaurants_data]
            print(f"Loaded {len(restaurants)} preprocessed restaurants.")
        else:
            print("Preprocessed dataset not found! Please run scripts/build_dataset.py first.")
            sys.exit(1)

        repository = RestaurantRepository(restaurants)
        
        engine = GroqRecommendationEngine()
        service = RecommendationService(repository=repository, engine=engine)
        
        # Attach to app state for routes to access
        app.state.repository = repository
        app.state.recommendation_service = service
        print("API services initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize API services: {e}")
        sys.exit(1)
        
    yield
    # Shutdown: Clean up if necessary
    print("Shutting down API...")

app = FastAPI(
    title="Restaurant Recommendation API", 
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.include_router(router, prefix="/api")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

# Mount frontend directory to serve the rest of the static assets
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
