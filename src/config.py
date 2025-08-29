import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "") # Load from .env or set directly
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")  # Default LLM or override in .env
YOUTUBE_VIDEO_ID = os.getenv("YOUTUBE_VIDEO_ID", "mdqb3fVqZgM")  # Default or override in .env

# Project root is one level up from src/
PROJECT_ROOT = Path(__file__).resolve().parent.parent  

DATA_DIR = PROJECT_ROOT / "data"
RAW_TRANSCRIPTS_DIR = DATA_DIR / "raw" / "transcripts"
PREPROCESSED_TRANSCRIPTS_DIR = DATA_DIR / "preprocessed" / "transcripts"
PERSONAS_DIR = DATA_DIR / "preprocessed" / "personas"
