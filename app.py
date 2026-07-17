import streamlit as st
import pandas as pd
import requests
import pickle

# Load the processed data and similarity matrix
import os
import urllib.request

if not os.path.exists("movie_data.pkl"):
    urllib.request.urlretrieve("https://drive.google.com/file/d/1zIQ0eHuebxMZ4h5jHqQKqB0IttAxOK1G/view?usp=drive_link", "movie_data.pkl")
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]




TMDB_API_KEY = st.secrets["TMDB_API_KEY"]  # Replace with your actual key



TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER = "https://via.placeholder.com/500x750?text=No+Poster"

def fetch_poster(movie_id):
    if movie_id is None:
        return PLACEHOLDER

    url = f"https://api.themoviedb.org/3/movie/{int(movie_id)}"

    params = {
        "api_key": TMDB_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            print("TMDB Error:", response.status_code, movie_id)
            return PLACEHOLDER

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return TMDB_IMAGE_URL + poster_path

        return PLACEHOLDER

    except Exception as e:
        print(e)
        return PLACEHOLDER



# Streamlit UI
st.title("Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie:",
    movies['title'].values
)


if st.button('Recommend'):

    recommendations = get_recommendations(selected_movie)

    st.write("Top 10 recommended movies:")

    for i in range(0, 10, 5):

        cols = st.columns(5)

        for col, j in zip(cols, range(i, i + 5)):

            if j < len(recommendations):

                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']

                poster_url = fetch_poster(movie_id)

                with col:
                    st.image(
                        poster_url,
                        width=130
                    )
                    st.write(movie_title)
