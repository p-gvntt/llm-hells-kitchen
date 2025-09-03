# Chef Inferno 🔥👨‍🍳

An AI-powered culinary experience that transforms a well-know celebrity chef into personalized recipe critiques. Using advanced NLP and the ML Food Buddy recommendation system, this project creates an authentic chef persona from a YouTube transcript and delivers brutally honest (yet helpful) cooking advice.

## ✨ Features

- **Persona Generation**: Extracts a well-know celebrity chef's personality from a Youtube transcript using GPT-4
- **Recipe Intelligence**: Integrates with ML Food Buddy's 500K+ recipe database
- **Authentic Critique**: Delivers personalized cooking advice in Chef Inferno's signature style
- **Smart Transcript Processing**: Automatically cleans and processes YouTube transcripts
- **Persistent Personas**: Save and reuse chef personalities across sessions
- **Interactive Web App**: Clean Streamlit interface for real-time chef critiques
- **Interactive Jupyter Demo**: Explore the system with an easy-to-use notebook interface
- **Demo Documentation**: HTML demo page with video walkthrough

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- **ML Food Buddy Recommender** (sister project - MUST be fully set up)
- ~2GB free disk space (for ML Food Buddy dataset and vectors)
- Internet connection for YouTube transcript fetching

### Installation

1. **Check your environment**
   ```bash
   python3 --version  # Should be 3.8+
   pip3 --version
   ```

2. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/llm-chef-inferno.git
   cd llm-chef-inferno
   ```

3. **Set up the ML Food Buddy dependency (CRITICAL)**
   ```bash
   # Clone the ML Food Buddy Recommender in the parent directory
   cd ..
   git clone https://github.com/yourusername/ml-food-buddy-recommender.git
   cd ml-food-buddy-recommender
   
   # Create virtual environment for ML Food Buddy
   python3 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install --upgrade pip
   pip install -r requirements.txt
   
   # Download the Food.com dataset (704MB)
   Visit: https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews
   Download recipes.csv and place in data/raw/recipes.csv
   
   # REQUIRED: Generate preprocessed data and TF-IDF vectors
   python -c "from src.preprocessing import preprocess_and_save; preprocess_and_save()"
   python -c "from src.vectorizer import train_and_save_vectorizer; train_and_save_vectorizer()"
   
   # Verify setup - these files should exist:
   # - data/raw/recipes.csv
   # - data/preprocessed/final_recipes.csv.gzip
   # - models/tfidf_vectorizer.pkl  
   # - models/recipe_vectors.npy
   
   deactivate  # Exit ML Food Buddy environment
   # Return to Chef Inferno project
   ```

4. **Configure environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. **Configure environment**I

Create a .env file in the project root and add the required environment variables:

Create the env file
```bash
touch .env
```

Open .env in a text editor and add your variables. For example:
```
OPENAI_API_KEY=your_api_key_here
DEFAULT_MODEL=gpt-4
```

Make sure to replace these values with yours.

7. **Launch the web app**
   ```bash
   streamlit run app/app.py
   ```

8. **Or try the interactive demo**
   ```bash
   jupyter notebook notebooks/chef_inferno_demo.ipynb
   ```

## 📁 Project Structure

```
llm-chef-inferno/
├── app/
│   └── app.py                   # Streamlit web application
├── data/
│   ├── raw/
│   │   └── transcripts/         # Raw YouTube transcripts
│   └── preprocessed/
│       ├── transcripts/         # Cleaned transcript files
│       └── personas/            # Generated chef personalities
├── docs/
│   ├── index.html               # Demo documentation page
│   └── media/                   # Demo videos and assets
├── notebooks/
│   └── chef_inferno_demo.ipynb  # Interactive demo
├── src/
│   ├── chef_rag.py             # Core Chef Inferno class
│   ├── chef_service.py         # End-to-end service orchestration
│   ├── config.py               # Project configuration
│   ├── food_buddy_api.py       # ML Food Buddy integration
│   └── transcript_utils.py     # YouTube transcript processing
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
└── README.md                  # Project documentation
```

## 🔧 How It Works

### 1. Transcript Acquisition
- Fetches YouTube transcripts using `youtube-transcript-api`
- Automatically handles video ID extraction and API calls
- Stores raw transcripts for reference and reprocessing

### 2. Persona Generation
- Uses GPT-4 to analyze a well-known celebrity chef's speaking patterns
- Creates concise, authentic personality descriptions 
- Captures speaking style, attitude, temperament, and reaction patterns
- Saves personas for consistent reuse across sessions

### 3. Recipe Recommendation
- Integrates with ML Food Buddy's TF-IDF-powered recommendation engine
- Processes user queries for ingredient matching and dietary preferences
- Returns top-ranked recipes with detailed nutritional information

### 4. Authentic Critique
- Combines chef persona with recipe data using structured prompting
- Generates responses that maintain character consistency
- Follows a well-known celebrity chef's signature style: criticism → guidance → encouragement

## 💻 Usage Examples

### Web Application

```bash
# Launch the Streamlit app
streamlit run app/app.py

# Then interact with the web interface:
# 1. Enter a YouTube video ID (or use default selected video)
# 2. Type your recipe query (e.g., "pasta with chicken")
# 3. Get authentic Chef Inferno critique in real-time
```

### Jupyter Notebook

```bash
# Launch and run the interactive demo - to run the demo, open this notebook:
jupyter notebook notebooks/chef_inferno_demo.ipynb

# Follow the step-by-step tutorial to:
# - Process Youtube transcripts
# - Generate chef personas
# - Get recipe recommendations
# - Experience authentic critiques
```

### Recipe Integration

```python
from src.food_buddy_api import get_food_buddy_recommendations

# Get personalized recipe recommendations
recipes = get_food_buddy_recommendations(
    query="healthy chicken dinner",
    time_pref="fast",      # fast/medium/long
    calorie_pref="low",    # low/medium/high
    top_n=1
)
```

## 🎬 Demo & Documentation

### Live Demo
Open `docs/index.html` in your browser to view the complete video walkthrough showing:
- Real-time transcript processing
- Persona generation from a Youtube video
- Recipe recommendation integration
- Authentic Chef Inferno critique generation

### Interactive Experience
The Streamlit web app provides an intuitive interface where you can:
- Input any YouTube video ID
- Enter recipe queries in natural language
- Watch as the AI processes transcripts and generates personas
- Receive personalized cooking critiques in a well-known celebrity chef signature style

## 🎯 Key Components
- **Persona Management**: Create, save, and load chef personalities
- **Recipe Critique**: Generate authentic responses using persona + recipe data
- **OpenAI Integration**: Seamless GPT model interaction with error handling

### Streamlit Web Interface
- **Real-time Processing**: Live transcript fetching and persona generation
- **User-friendly UI**: Clean, intuitive interface for non-technical users
- **Interactive Feedback**: Step-by-step processing visualization
- **Responsive Design**: Works across desktop and mobile devices

### Smart Transcript Processing
- **Auto-cleaning**: Converts raw transcripts to natural, punctuated prose
- **Truncation Safety**: Handles large transcripts within token limits
- **Dual Storage**: Maintains both raw and processed versions

### ML Food Buddy Integration
- **Isolated Loading**: Prevents module conflicts between projects
- **Path Management**: Handles complex inter-project dependencies
- **Error Recovery**: Robust environment restoration after API calls

## 📊 Supported Video Sources

The system works with any Youtube video available with transcripts:

- **Season Episodes**: Full episode transcripts for comprehensive persona building
- **Highlights**: Shorter clips focusing on specific cooking moments
- **Challenges**: Competition episodes showcasing different chef personalities
- **Restaurant Service**: High-pressure kitchen environments

## 🛠️ Development

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
OPENAI_MODEL=gpt-4o                    # Default: gpt-4o
YOUTUBE_VIDEO_ID=mdqb3fVqZgM          # Default video for demos
```

## 🤝 Integration Guide

### With ML Food Buddy Recommender

This project **requires** the ML Food Buddy Recommender to be fully operational with:

```bash
# Required directory structure:
parent_directory/
├── llm-chef-inferno/
└── ml-food-buddy-recommender/
    ├── data/
    │   ├── raw/recipes.csv              # 704MB dataset
    │   └── preprocessed/
    │       └── recipes_processed.csv    # Generated by preprocessing
    ├── models/
    │   ├── tfidf_vectorizer.pkl        # Trained TF-IDF model
    │   └── recipe_vectors.npy          # Precomputed recipe vectors
    └── src/                            # ML Food Buddy source code
```

**Critical Setup Steps:**
1. Download Food.com recipes dataset (704MB)
2. Run preprocessing pipeline to clean and prepare data
3. Train TF-IDF vectorizer on 500K+ recipes
4. Generate recipe similarity vectors for fast lookups

The integration handles:
- **Module Isolation**: Prevents import conflicts between projects
- **Path Management**: Dynamic path resolution and environment switching
- **Data Pipeline**: Seamless recipe data flow from vectors to critiques
- **Error Recovery**: Automatic environment restoration after API calls

## 🚨 Troubleshooting

### Common Issues

**OpenAI API Errors:**
- Verify API key in `.env` file
- Check account billing and rate limits
- Ensure model availability (gpt-4o, gpt-3.5-turbo)

**ML Food Buddy Not Set Up:**
- Ensure you've downloaded the 704MB recipes.csv dataset
- Verify preprocessing completed: `data/preprocessed/recipes_processed.csv` exists
- Confirm vectorizer trained: `models/tfidf_vectorizer.pkl` and `models/recipe_vectors.npy` exist
- Check ML Food Buddy virtual environment is properly configured

**Transcript Processing:**
- Ensure YouTube video has captions enabled
- Try different video IDs if transcripts unavailable
- Check internet connectivity for API calls

**Memory Issues:**
- Large transcripts are automatically truncated
- Clear persona cache if running multiple demos
- Monitor token usage with large recipe databases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI**: GPT models for persona generation and critique
- **YouTube Transcript API**: Automated transcript extraction
- **Food.com Dataset**: 500K+ recipes for recommendation training

---

**"Right, you muppet! Follow the bloody instructions and you might actually cook something decent!"** 🔥

*Ready to get roasted by the best AI celebrity Chef? Fire up the notebook and buon appetito!* 👨‍🍳✨