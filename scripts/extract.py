import zipfile
import os

zip_path = r"d:\Cursor Projects\stitch_gastroai_premium_recommender.zip"
extract_path = r"d:\Cursor Projects\frontend"

os.makedirs(extract_path, exist_ok=True)
try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Extracted successfully")
except Exception as e:
    print(f"Error extracting: {e}")
