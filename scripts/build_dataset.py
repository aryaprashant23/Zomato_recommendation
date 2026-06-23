
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from app.data.loader import DatasetLoader
from app.data.preprocessor import DataPreprocessor

print('Loading raw dataset...')
loader = DatasetLoader('d:/Cursor Projects/data/zomato_cache.parquet')
df = loader.load_raw_dataset()
print('Preprocessing...')
preprocessor = DataPreprocessor()
restaurants = preprocessor.preprocess(df)
print(f'Extracted {len(restaurants)} restaurants.')

out_path = 'd:/Cursor Projects/data/restaurants_processed.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump([r.model_dump() for r in restaurants], f)
print(f'Saved to {out_path}')

