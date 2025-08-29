import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")  # Default LLM

DATA_DIR = "data"
RAW_TRANSCRIPTS_DIR = os.path.join(DATA_DIR, "raw", "transcripts")
PREPROCESSED_TRANSCRIPTS_DIR = os.path.join(DATA_DIR, "preprocessed", "transcripts")
PERSONAS_DIR = os.path.join(DATA_DIR, "preprocessed", "personas")

# Ensure folders exist
for folder in [RAW_TRANSCRIPTS_DIR, PREPROCESSED_TRANSCRIPTS_DIR, PERSONAS_DIR]:
    os.makedirs(folder, exist_ok=True)
