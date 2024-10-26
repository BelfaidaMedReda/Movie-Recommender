#!/usr/bin/env python3
import pandas as pd
import streamlit as st
from ipynb.fs.full.main import *
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def get_image(movie):
    index = movies.index[movies["title"] == movie][0]
    movie_id = movies.iloc[index]["id"]
    return fetch_poster(movie_id)



def main():
    # Custom CSS to style the header and elements
    st.markdown(
        """
        <style>
        /* Center and enlarge the header with green color */
        .header-style {
            font-size: 40px;  /* Increase font size */
            font-weight: bold;
            color: green;     /* Set text color to green */
            text-align: center;
        }

        /* Style the select box */
        .css-19fzk5d {  /* Selectbox class; Streamlit class names may vary by version */
            font-size: 18px;
            text-align: center;
        }

        /* Center the button */
        .stButton > button {
            display: block;
            margin: 0 auto;
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Centered Header
    st.markdown('<h1 class="header-style">Movies Recommendation System App</h1>', unsafe_allow_html=True)

    # Selectbox for movie selection
    option = st.selectbox(
        "Choose your preferred movie",
        movies["title"],
    )

    # Centered Recommend Button
    button = st.button("Recommend")

    if button:
        recommended_movies = recommend(option)
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(recommended_movies[0])
            st.image(get_image(recommended_movies[0]))
        
        with col2:
            st.text(recommended_movies[1])
            st.image(get_image(recommended_movies[1]))

        with col3:
            st.text(recommended_movies[2])
            st.image(get_image(recommended_movies[2]))

        with col4:
            st.text(recommended_movies[3])
            st.image(get_image(recommended_movies[3]))
        
        with col5:
            st.text(recommended_movies[4])
            st.image(get_image(recommended_movies[4]))


if __name__=="__main__":
    main()