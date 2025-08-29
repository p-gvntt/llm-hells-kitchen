import os
from openai import OpenAI
from config import OPENAI_API_KEY, RAW_TRANSCRIPTS_DIR, PREPROCESSED_TRANSCRIPTS_DIR, DEFAULT_MODEL

def save_file(text, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def clean_transcript_text(transcript_text: str, file_name: str, model: str = None) -> str:
    """
    Rewrite transcript into natural, punctuated language and save to preprocessed folder.
    """
    model = model or DEFAULT_MODEL
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Save raw transcript
    raw_path = os.path.join(RAW_TRANSCRIPTS_DIR, f"{file_name}.txt")
    save_file(transcript_text, raw_path)

    # Truncate for safety
    if len(transcript_text) > 3000:
        transcript_text = transcript_text[:3000] + "..."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a transcript editor. Rewrite text into smooth, natural English prose "
                        "with correct punctuation, keeping the original tone and style. "
                        "Do not summarize or remove content."
                    )
                },
                {"role": "user", "content": transcript_text}
            ],
            max_tokens=800,
            temperature=0.5
        )

        cleaned_text = response.choices[0].message.content.strip()

        # Save preprocessed transcript
        preprocessed_path = os.path.join(PREPROCESSED_TRANSCRIPTS_DIR, f"{file_name}_clean.txt")
        save_file(cleaned_text, preprocessed_path)

        return cleaned_text

    except Exception as e:
        return f"❌ Transcript cleaning failed: {str(e)}"