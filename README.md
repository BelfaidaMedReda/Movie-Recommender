# Movie Recommendation System

## Overview
A content-based movie recommendation system that suggests similar movies based on movie descriptions, genres, cast, crew, and keywords. The system uses natural language processing (NLP) techniques and machine learning to provide personalized movie recommendations through an interactive Streamlit web interface.

## Features
- Content-based movie recommendation using multiple movie attributes
- Interactive web interface built with Streamlit
- Real-time movie poster fetching from TMDB API
- Processes movie metadata including:
  - Genres
  - Keywords
  - Cast (top 3 actors)
  - Director
  - Overview
  - Movie descriptions

## Technical Architecture
- **Data Processing**: 
  - Text preprocessing using NLTK
  - Porter Stemming for word normalization
  - Stop words removal
  - Punctuation handling
  
- **Feature Engineering**:
  - Text vectorization using CountVectorizer
  - Custom StemmedCountVectorizer implementation
  - Bag of Words (BOW) representation
  
- **Similarity Calculation**:
  - Cosine similarity for movie comparison
  - Top 5 similar movies recommendation


- **Designed a Movie Recommendation System Interface**:
  - Developed a user-friendly interface using **Streamlit** to create an interactive web app.
  - Implemented a **dropdown selection** for users to choose their preferred movie.

- **Implemented API Integration**:
  - Integrated the **TMDB API** to fetch movie data, including titles and poster images.
  - Defined a function `fetch_poster()` to retrieve movie posters dynamically based on movie ID.

- **Recommendation Functionality**:
  - Developed a custom recommendation engine using preprocessed data to suggest similar movies.
  - Displayed recommended movies and their posters in a **grid format** using Streamlit columns.

- **Responsive Design**: 
  - Styled interface with customized headers and buttons


## Installation

1. Clone the repository :
```bash
git clone <repository-url>
```
2. Install dependencies :
```bash
pip install -r requirements.txt
```

3. Set up TMDB API key :
```bash
export TMDB_API_KEY='403a18b0032fe0e147157809530a8230'
```

4. Run the application :
```bash
streamlit run app.py
```

## Project Structure
``` bash
├── app.py               # Streamlit web interface
├── main.py             # Core recommendation logic
├── requirements.txt    # Project dependencies
├── dataset/
│   ├── movies.csv     # Movie metadata
│   └── credits.csv    # Cast and crew information
```
## How It Works

1. Data Processing Phase:
    - Loads and merges movie datasets
    - Extracts and processes movie features
    - Creates a unified tag system for each movie

2. Feature Engineering Phase:
    - Converts text data into numerical format
    - Creates movie vectors using BOW approach
    - Implements text stemming and stop word removal

3. Recommendation Phase:
    - Calculates similarity between movies
    - Selects top 5 most similar movies
    - Fetches and displays movie posters

4. Application Development
    - Styled interface with customized headers and buttons

## Simulation 