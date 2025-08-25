import sys
from pathlib import Path
import importlib.util
import numpy as np
import pandas as pd

# Path configuration
BASE_PARENT = Path(__file__).resolve().parent.parent.parent
RECOMMENDER_PATH = BASE_PARENT / "ml-food-buddy-recommender" / "src" / "recommender.py"
ML_BUDDY_PATH = BASE_PARENT / "ml-food-buddy-recommender"
if not RECOMMENDER_PATH.exists():
    raise FileNotFoundError(f"Cannot find recommender.py at {RECOMMENDER_PATH}")

# Add to Python path and load module
sys.path.insert(0, str(ML_BUDDY_PATH))
spec = importlib.util.spec_from_file_location("recommender", RECOMMENDER_PATH)
recommender = importlib.util.module_from_spec(spec)
sys.modules["recommender"] = recommender

# Temporarily modify sys.path for import
original_path = sys.path.copy()
try:
    sys.path.insert(0, str(ML_BUDDY_PATH))
    spec.loader.exec_module(recommender)
finally:
    sys.path = original_path

# Load artifacts
df, vectorizer, vectors = recommender.load_artifacts()

# Recommendation function
def get_food_buddy_recommendations(query, time_pref=None, calorie_pref=None, top_n=3):
    results = recommender.recommend(
        user_prefs=query,
        dataset=df,
        recipe_vectors_matrix=vectors,
        vectorizer=vectorizer,
        top_n=top_n,
        time_pref=time_pref,
        calorie_pref=calorie_pref,
        return_columns=[
            "Name", "Image_first", "TotalTime_str",
            "recipe_instructions_clean", "ingredients_clean", "Calories", "similarity"
        ]
    )
    # Clean results
    results_clean = (
        results.drop_duplicates(subset=["Name"])
               .head(top_n)
               .replace({np.nan: None, np.inf: None, -np.inf: None})
    )
    # Convert numeric columns
    for col in ["Calories", "similarity"]:
        if col in results_clean.columns:
            results_clean[col] = results_clean[col].apply(
                lambda x: float(x) if x is not None else None
            )
    return results_clean.to_dict(orient="records")