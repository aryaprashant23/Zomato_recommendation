"""
Smoke test script to verify Phase 1: Data Ingestion.
Loads the dataset, cleans/normalizes it, and prints database summary statistics.
"""
import sys
import os

# Add project root to python path to run script directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.data.loader import DatasetLoader
from app.data.preprocessor import DataPreprocessor
from app.data.repository import RestaurantRepository


def run_smoke_test():
    print("--- Phase 1: Data Ingestion Smoke Test ---")
    print(f"Dataset Cache Path: {settings.DATASET_CACHE_PATH}")
    
    loader = DatasetLoader(settings.DATASET_CACHE_PATH)
    preprocessor = DataPreprocessor()
    
    print("\n[1/3] Loading dataset from Hugging Face or local cache...")
    try:
        raw_df = loader.load_raw_dataset()
        print(f"Successfully loaded {len(raw_df)} raw records.")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        sys.exit(1)
        
    print("\n[2/3] Preprocessing and normalizing data...")
    try:
        restaurants = preprocessor.preprocess(raw_df)
        print(f"Preprocessing completed. {len(restaurants)} canonical records remaining after deduplication.")
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        sys.exit(1)

    print("\n[3/3] Building in-memory repository...")
    repo = RestaurantRepository(restaurants)
    locations = repo.get_locations()
    cuisines = repo.get_cuisines()
    
    print(f"Distinct locations found: {len(locations)}")
    print(f"Distinct cuisines found: {len(cuisines)}")
    
    if restaurants:
        print("\n--- Sample Restaurant Record ---")
        sample = restaurants[0]
        print(f"ID: {sample.id}")
        print(f"Name: {sample.name}")
        print(f"Location: {sample.location}")
        print(f"Cuisines: {sample.cuisines}")
        print(f"Rating: {sample.rating}")
        print(f"Cost for two: {sample.cost_for_two}")
        print(f"Budget Tier: {sample.budget_tier}")
        print(f"Online Order: {sample.online_order}")
        print(f"Book Table: {sample.book_table}")
        print(f"Votes: {sample.votes}")
    else:
        print("\nWarning: No restaurants were processed.")
        
    print("\nSmoke test finished successfully!")


if __name__ == "__main__":
    run_smoke_test()
