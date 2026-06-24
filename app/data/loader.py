import os
from datasets import load_dataset
import pandas as pd


class DatasetLoader:
    """
    Handles connection and fetching of raw restaurant records from Hugging Face Hub,
    or falls back to local Parquet cache if offline.
    """
    def __init__(self, cache_path: str):
        self.cache_path = cache_path

    def load_raw_dataset(self) -> pd.DataFrame:
        """
        Loads dataset from Hugging Face or local cache.
        Returns:
            pd.DataFrame: Raw data rows.
        """
        if os.path.exists(self.cache_path):
            try:
                return pd.read_parquet(self.cache_path)
            except Exception:
                # If reading cache fails, we will try to load from HF Hub
                pass

        try:
            dataset_dict = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
            if "train" in dataset_dict:
                df = dataset_dict["train"].to_pandas()
            else:
                first_split = list(dataset_dict.keys())[0]
                df = dataset_dict[first_split].to_pandas()

            # Ensure data cache directory exists
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            df.to_parquet(self.cache_path, index=False)
            return df
        except Exception as e:
            # Last-resort fallback to cache if HF loading fails
            if os.path.exists(self.cache_path):
                return pd.read_parquet(self.cache_path)
            raise RuntimeError(
                f"Failed to load dataset from Hugging Face and no local cache was found. Error: {e}"
            )

