import sys
import os
from pathlib import Path
import importlib.util
import numpy as np
import pandas as pd

# Path configuration
BASE_PARENT = Path(__file__).resolve().parent.parent.parent
ML_BUDDY_PATH = BASE_PARENT / "ml-food-buddy-recommender"
ML_BUDDY_SRC_PATH = ML_BUDDY_PATH / "src"
RECOMMENDER_PATH = ML_BUDDY_SRC_PATH / "recommender.py"
UTILS_PATH = ML_BUDDY_SRC_PATH / "utils.py"
CONFIG_PATH = ML_BUDDY_SRC_PATH / "config.py"

if not all(p.exists() for p in [RECOMMENDER_PATH, UTILS_PATH, CONFIG_PATH]):
    raise FileNotFoundError("Cannot find required ML buddy modules")

# Store original state
original_cwd = os.getcwd()
original_path = sys.path.copy()

def load_ml_buddy_modules():
    """Load ML buddy modules in isolation"""
    # Clear conflicting modules and change to project directory
    modules_to_remove = [k for k in sys.modules.keys() if k.startswith('src.')]
    for module in modules_to_remove:
        del sys.modules[module]
    
    os.chdir(ML_BUDDY_PATH)
    
    # Preserve standard library and essential paths
    stdlib_paths = [p for p in sys.path if 'site-packages' not in p and 'lib/python' in p]
    site_packages = [p for p in sys.path if 'site-packages' in p]
    
    sys.path.clear()
    # Add our paths first, then standard library, then site-packages
    sys.path.extend([str(ML_BUDDY_PATH), str(ML_BUDDY_SRC_PATH)])
    sys.path.extend(stdlib_paths)
    sys.path.extend(site_packages)
    
    # Load modules in correct order
    for name, path in [("src.utils", UTILS_PATH), ("src.config", CONFIG_PATH), ("recommender", RECOMMENDER_PATH)]:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    
    # Load artifacts and return everything needed
    recommender = sys.modules["recommender"]
    df, vectorizer, vectors = recommender.load_artifacts()
    return recommender, df, vectorizer, vectors

try:
    recommender, df, vectorizer, vectors = load_ml_buddy_modules()
finally:
    # Restore original environment
    os.chdir(original_cwd)
    sys.path.clear()
    sys.path.extend(original_path)

# Recommendation function
def get_food_buddy_recommendations(query, time_pref=None, calorie_pref=None, top_n=3):
    current_cwd = os.getcwd()
    current_path = sys.path.copy()
    
    try:
        os.chdir(ML_BUDDY_PATH)
        sys.path.insert(0, str(ML_BUDDY_PATH))
        
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
    finally:
        os.chdir(current_cwd)
        sys.path.clear()
        sys.path.extend(current_path)
    
    # Clean and return results
    results_clean = (
        results.drop_duplicates(subset=["Name"])
        .head(top_n)
        .replace({np.nan: None, np.inf: None, -np.inf: None})
    )
    
    for col in ["Calories", "similarity"]:
        if col in results_clean.columns:
            results_clean[col] = results_clean[col].apply(
                lambda x: float(x) if x is not None else None
            )
    
    return results_clean.to_dict(orient="records")