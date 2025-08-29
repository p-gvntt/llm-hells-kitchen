import os
from openai import OpenAI
from .config import OPENAI_API_KEY, PERSONAS_DIR, DEFAULT_MODEL

class HellKitchenChef:
    def __init__(self, model: str = None):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model or DEFAULT_MODEL
        self.chef_persona = None

    def save_persona(self, persona_text, file_name):
        path = os.path.join(PERSONAS_DIR, f"{file_name}_persona.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(persona_text)
        return path

    def load_persona(self, file_name):
        path = os.path.join(PERSONAS_DIR, f"{file_name}_persona.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.chef_persona = f.read()
                return self.chef_persona
        return None

    def create_persona_from_transcript(self, transcript_text: str, file_name: str, model: str = None) -> str:
        if self.chef_persona:
            return self.chef_persona  # Already loaded

        model = model or self.model

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a chef personality analyzer. Create concise, accurate personality descriptions."},
                    {"role": "user", "content": transcript_text}
                ],
                max_tokens=300,
                temperature=0.7
            )
            persona_text = response.choices[0].message.content.strip()
            self.chef_persona = persona_text
            self.save_persona(persona_text, file_name)
            return persona_text
        except Exception as e:
            return f"❌ Persona generation failed: {str(e)}"

    def critique_recipe(self, recipe_data, user_query: str, model: str = None) -> str:
        if not self.chef_persona:
            return "❌ Create persona first"

        model = model or self.model

        if isinstance(recipe_data, list):
            recipe_data = recipe_data[0] if recipe_data else {}

        recipe_name = recipe_data.get("Name", recipe_data.get("name", "Unknown Recipe"))
        ingredients = recipe_data.get("ingredients_clean", recipe_data.get("ingredients", "No ingredients"))
        instructions = recipe_data.get("recipe_instructions_clean", recipe_data.get("instructions", "No instructions"))

        if len(ingredients) > 1000: ingredients = ingredients[:1000] + "..."
        if len(instructions) > 1500: instructions = instructions[:1500] + "..."

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You are a chef with this exact personality: {self.chef_persona}"},
                    {"role": "user", "content": f"""User request: "{user_query}"
Recipe: {recipe_name}
Ingredients: {ingredients}
Instructions: {instructions}
Respond in character."""}
                ],
                max_tokens=600,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ Recipe critique failed: {str(e)}"