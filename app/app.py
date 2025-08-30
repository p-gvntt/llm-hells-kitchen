import streamlit as st
import sys
import os
import time
from pathlib import Path
from PIL import Image
import pandas as pd

# Path setup
project_root = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path().resolve().parent
src_path = project_root / "src"
sys.path.append(str(src_path))

# Local modules
from transcript_utils import clean_transcript_text
from chef_rag import HellKitchenChef
from chef_service import generate_chef_response
from config import (
    YOUTUBE_VIDEO_ID,
    DEFAULT_MODEL,
    RAW_TRANSCRIPTS_DIR,
    PREPROCESSED_TRANSCRIPTS_DIR,
    PERSONAS_DIR,
)

# Page configuration
st.set_page_config(
    page_title="Hell's Kitchen Chef",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .chef-container {
        display: flex;
        align-items: flex-start;
        gap: 20px;
        margin: 20px 0;
    }
    
    .chef-image {
        flex-shrink: 0;
    }
    
    .chef-response {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4444;
        flex-grow: 1;
        position: relative;
    }
    
    .reset-button {
        background-color: #ff6b6b !important;
        color: white !important;
        margin-top: 20px;
    }
    
    .typing-cursor {
        display: inline-block;
        width: 2px;
        height: 1em;
        background-color: #000;
        margin-left: 2px;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
</style>
""", unsafe_allow_html=True)

def load_chef_image():
    """Load Hell's Kitchen Chef image with relative path"""
    try:
        # Try to get the image using a relative path
        current_dir = Path(__file__).parent if "__file__" in globals() else Path.cwd()
        image_path = current_dir / "media" / "chef.webp"
        
        if image_path.exists():
            return Image.open(image_path)
        else:
            # If not found, try an alternative approach
            try:
                # Try one level up (if running from src)
                image_path = current_dir.parent / "media" / "chef.webp"
                if image_path.exists():
                    return Image.open(image_path)
            except Exception:
                pass
            
            st.error(f"Image not found at: {image_path}")
            return None
    except Exception as e:
        st.error(f"Could not load Chef's image: {e}")
        return 

def reset_conversation():
    """Reset the conversation state"""
    st.session_state.conversation_started = False
    st.session_state.chef_response = ""
    st.session_state.user_ingredients = ""
    st.session_state.typing_complete = False
    st.session_state.typing_progress = 0

def simulate_typing(text, speed=50):
    """Simulate typing effect by displaying text character by character"""
    placeholder = st.empty()
    typed_text = ""
    
    for i, char in enumerate(text):
        typed_text += char
        # Add a blinking cursor at the end
        display_text = typed_text + '<span class="typing-cursor"></span>'
        placeholder.markdown(f'<div class="chef-response">{display_text}</div>', unsafe_allow_html=True)
        
        # Update session state with progress
        st.session_state.typing_progress = i + 1
        
        # Adjust speed for punctuation - reduced delays for faster typing
        if char in ".!?":
            time.sleep(0.1) 
        elif char == ",":
            time.sleep(0.05) 
        else:
            time.sleep(1/speed)
    
    # Remove cursor and show final text
    placeholder.markdown(f'<div class="chef-response">{typed_text}</div>', unsafe_allow_html=True)
    st.session_state.typing_complete = True

# Main app
def main():
    # Header
    st.title("🔥 Hell's Kitchen Chef")
    st.markdown("*Get cooking advice from our fiery chef!*")
    
    # Hidden configuration - use defaults
    model = DEFAULT_MODEL
    video_id = YOUTUBE_VIDEO_ID
    
    # Initialize session state
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False
    if "chef_response" not in st.session_state:
        st.session_state.chef_response = ""
    if "user_ingredients" not in st.session_state:
        st.session_state.user_ingredients = ""
    if "typing_complete" not in st.session_state:
        st.session_state.typing_complete = False
    if "typing_progress" not in st.session_state:
        st.session_state.typing_progress = 0
    if "recipe_error" not in st.session_state:
        st.session_state.recipe_error = False
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        chef_image = load_chef_image()
        if chef_image:
            st.image(chef_image, caption="Hell's Kitchen Chef", width=200)
        else:
            st.markdown("👨‍🍳")
            st.caption("*Hell's Kitchen Chef*")
    
    with col2:
        if not st.session_state.conversation_started:
            # Show greeting
            st.markdown(f"""
            <div class="chef-response">
                <strong>Chef:</strong><br>
                "Oi, you muppet! I hear you're trying to cook something. Pathetic! Let me save your sorry attempt by actually suggesting some proper recipes. Now, cough up those ingredients before you ruin dinner, and I'll show you how to turn that mess into something absolutely stunning — got it?"
            </div>
            """, unsafe_allow_html=True)
            
            # User input
            user_ingredients = st.text_area(
                "Your ingredients:",
                value=st.session_state.user_ingredients,
                placeholder="e.g., chicken breast, pasta, garlic, tomatoes, parmesan cheese...",
                height=100,
                help="Tell our chef what ingredients you have available",
                key="ingredients_input"
            )
            
            # Generate response button
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button("🔥 Get Chef's Advice!", type="primary", use_container_width=True):
                    if not user_ingredients.strip():
                        st.warning("⚠️ Please enter some ingredients first!")
                        return
                    
                    # Store the ingredients
                    st.session_state.user_ingredients = user_ingredients
                    user_query = user_ingredients
                    
                    with st.spinner("Chef is thinking..."):
                        try:
                            result = generate_chef_response(
                                video_id=video_id, 
                                user_query=user_query, 
                                model=model
                            )
                            
                            # Check for errors in the response
                            if "error" in result:
                                st.session_state.chef_response = "Sorry, I don't have anything in mind for those ingredients. Try with something else!"
                                st.session_state.conversation_started = True
                                st.session_state.recipe_error = True
                                st.rerun()
                                return
                            
                            # Extract the critique from the response
                            chef_response = result.get("critique", "")
                            
                            if not chef_response:
                                st.session_state.chef_response = "Sorry, I don't have anything in mind for those ingredients. Try with something else!"
                                st.session_state.conversation_started = True
                                st.session_state.recipe_error = True
                                st.rerun()
                                return
                            
                            # Check if the chef couldn't find a recipe
                            if any(phrase in chef_response.lower() for phrase in ["sorry", "don't know", "can't", "no recipe", "not found"]):
                                st.session_state.chef_response = "Sorry, I don't have anything in mind for those ingredients. Try with something else!"
                                st.session_state.conversation_started = True
                                st.session_state.recipe_error = True
                                st.rerun()
                            else:
                                st.session_state.chef_response = chef_response
                                st.session_state.conversation_started = True
                                st.session_state.typing_complete = False
                                st.session_state.recipe_error = False
                                st.rerun()
                                
                        except Exception as e:
                            # Handle the specific error you mentioned
                            error_msg = str(e)
                            if "Index(['Name'], dtype='object')" in error_msg:
                                st.session_state.chef_response = "Sorry, I don't have anything in mind for those ingredients. Try with something else!"
                                st.session_state.conversation_started = True
                                st.session_state.recipe_error = True
                                st.rerun()
                            else:
                                st.error(f"⚠️ Something went wrong while generating the recipe: {error_msg}")

        else:
            # Show Chef's response with typing effect
            if st.session_state.chef_response:
                # If it's an error message, show it immediately without typing effect
                if st.session_state.recipe_error:
                    st.markdown(f"""
                    <div class="chef-response">
                        {st.session_state.chef_response}
                    </div>
                    """, unsafe_allow_html=True)
                # Otherwise, use typing effect for recipe
                else:
                    # If typing is not complete, simulate typing
                    if not st.session_state.typing_complete:
                        # Start from where we left off if any
                        text_to_type = st.session_state.chef_response
                        if st.session_state.typing_progress > 0:
                            text_to_type = text_to_type[st.session_state.typing_progress:]
                        
                        simulate_typing(text_to_type)
                    else:
                        # Show full response if typing is complete
                        st.markdown(f"""
                        <div class="chef-response">
                            {st.session_state.chef_response}
                        </div>
                        """, unsafe_allow_html=True)
            
            # Button to cook another recipe
            if st.button("🍳 Cook Another Recipe", type="primary", use_container_width=True, 
                         on_click=reset_conversation):
                pass

    # Footer
    st.markdown("---")
    st.markdown("*Built with Streamlit • Powered by OpenAI • Inspired by a famous fiery chef*")

if __name__ == "__main__":
    main()