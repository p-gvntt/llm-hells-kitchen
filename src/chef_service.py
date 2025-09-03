from transcript_utils import clean_transcript_text
from chef_rag import ChefInferno
from food_buddy_api import get_food_buddy_recommendations
from youtube_transcript_api import YouTubeTranscriptApi
from config import DEFAULT_MODEL

def generate_chef_response(video_id: str, user_query: str, model: str = None) -> dict:
    """
    Fetch transcript, create persona, get recipe, and generate critique.
    Returns a dict with persona, cleaned transcript, and critique.
    """
    model = model or DEFAULT_MODEL
    file_name = video_id

    # Fetch YouTube transcript
    try:
        api = YouTubeTranscriptApi()
        raw_transcript_obj = api.fetch(video_id)
        raw_text = " ".join([s.text for s in raw_transcript_obj])

    except Exception as e:
        return {"error": f"Failed to fetch transcript: {str(e)}"}

    # Clean transcript
    cleaned_text = clean_transcript_text(raw_text, file_name, model=model)

    # Instantiate Chef
    chef = ChefInferno(model=model)
    persona = chef.load_persona(file_name) or chef.create_persona_from_transcript(
        cleaned_text, file_name, model=model
    )

    # Fetch recipe
    recipe = get_food_buddy_recommendations(user_query)
    if not recipe:
        return {"error": "No recipe found"}

    # Generate critique
    critique = chef.critique_recipe(recipe[0], user_query, model=model)

    return {
        "persona": persona,
        "cleaned_transcript": cleaned_text,
        "critique": critique
    }
