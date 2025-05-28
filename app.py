import streamlit as st
import pickle
import pandas as pd
import requests
from fuzzywuzzy import fuzz, process

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MovieMine",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TMDb TOKEN ---
tmdb_token = st.secrets["tmdb_token"]

# --- LOCAL CSS & OPTIONAL BACKGROUND IMAGE ---
import base64

def get_base64(path):
    try:
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

# Loading 'bg.jpg' from current directory
bg_b64 = get_base64('pics/bg.jpg')

if bg_b64:
    bg_style = f"background-image: url('data:image/jpg;base64,{bg_b64}');"
else:
    bg_style = "background: linear-gradient(to right, #2c3e50, #4ca1af);"

st.markdown(
    f"""
    <style>
    #MainMenu, footer {{visibility: hidden;}}
    .stApp {{{bg_style} background-size: cover; background-position: center; color: #fff; padding-top:1rem;}}
    .title {{font-size:3rem; font-weight:bold; text-align:center; margin:20px 0; color:#ffcc00; text-shadow:2px 2px #00000050;}}
    .selected-movie {{background:rgba(0,0,0,0.6); border:2px solid #ffcc00; border-radius:15px; padding:15px; margin:10px 0;}}
    .selected-movie h3 {{color:#ffcc00; margin-bottom:5px;}} .selected-movie p {{color:#e0e0e0; font-size:0.9rem; margin:3px 0;}}
    .movie-card {{background:rgba(0,0,0,0.6); border:2px solid #ffcc00; border-radius:15px; overflow:hidden; margin:10px; text-align:center; transition:transform 0.2s; padding:10px;}}
    .movie-card:hover {{transform:scale(1.03);}} .movie-card img {{width:100%; border-radius:10px;}}
    .movie-card h4 {{margin:10px 0 5px; color:#ffcc00; font-size:1.1rem;}} .movie-card p {{color:#e0e0e0; font-size:0.9rem; margin:5px 0;}}
    </style>
    """,
    unsafe_allow_html=True
)

# --- TITLE ---
# --- TITLE & HEADER BOX ---
st.markdown(
    """
    <div style='max-width:600px; margin:10px auto 20px; padding:10px;
                background: rgba(0,0,0,0.8); border-left:4px solid #ffcc00;
                border-radius:8px; box-shadow: 0 3px 15px rgba(0,0,0,0.6);'>
        <h1 style='font-size:2.5rem; text-align:center; color:#ffcc00; margin:0;'>
            MovieMine 🎥
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)


# --- LOAD DATA ---
@st.cache_data
def load_movies():
    try:
        with open('movie_dict.pkl','rb') as f:
            return pd.DataFrame(pickle.load(f))
    except FileNotFoundError:
        st.error("❌ 'movie_dict.pkl' not found.")
        return pd.DataFrame()

@st.cache_data
def load_similarity():
    try:
        with open('similarity.pkl','rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error("❌ 'similarity.pkl' not found.")
        return None

movies = load_movies()
similarity = load_similarity()
if movies.empty or similarity is None:
    st.stop()

# --- TMDb DETAIL FETCHER ---
def fetch_movie_details(movie_id: int) -> dict:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_token}&language=en-US"
    resp = requests.get(url)
    resp.raise_for_status()
    d = resp.json()
    return {
        "title": d.get("title"),
        "overview": d.get("overview"),
        "release_date": d.get("release_date"),
        "rating": d.get("vote_average"),
        "poster_url": f"https://image.tmdb.org/t/p/w500{d.get('poster_path')}"
    }

# --- FUZZY SEARCH ---
def fuzzy_search_movies(query, movie_list, limit=5):
    if not query: return []
    matches = process.extract(query, movie_list, scorer=fuzz.partial_ratio, limit=limit)
    return [(t,s) for t,s in matches if s>=60]

# --- RECOMMENDATION LOGIC ---
def recommend_ids(movie_name: str, n=10):
    try:
        idx = movies[movies['title']==movie_name].index[0]
    except IndexError:
        return []
    sims = sorted(enumerate(similarity[idx]), key=lambda x:x[1], reverse=True)[1:n+1]
    return [movies.iloc[i].movie_id for i,_ in sims]

# --- SIDEBAR ---
st.sidebar.header("🔍 Search & Select")
if 'selected' not in st.session_state:
    st.session_state.selected = ''

# Fuzzy search input
g = st.sidebar.text_input("📽️ Search for a movie:", placeholder="Type a movie name...")
if g:
    results = fuzzy_search_movies(g, movies['title'].tolist(), limit=8)
    if results:
        st.sidebar.markdown("### 🎯 Results")
        for idx, (title, score) in enumerate(results):
            if st.sidebar.button(f"{title} ({score}%)", key=f"search_{idx}_{title}"):
                st.session_state.selected = title
    else:
        st.sidebar.warning("No matches found.")

# Browse dropdown
titles = ["🔍 Browse a movie..."] + movies['title'].tolist()
choice = st.sidebar.selectbox("📋 Or browse all:", titles)

# Only update session state if a real movie is selected
if choice != "🔍 Browse a movie...":
    st.session_state.selected = choice


# Clear selection and slider
t = st.sidebar.slider("📊 Recommendations", 5, 20, 10, 5)
if st.session_state.selected:
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ Clear Selection"):
        st.session_state.selected = ''

# --- MAIN CONTENT ---
if st.session_state.selected:
    det = fetch_movie_details(
        movies.loc[movies['title']==st.session_state.selected, 'movie_id'].iloc[0]
    )
    st.markdown("### 🎬 Selected Movie")
    c1, c2 = st.columns([1,3])
    with c1:
        st.image(det['poster_url'], width=200)
    with c2:
        st.markdown(
            f"<div class='selected-movie'>"
            f"<h3>{det['title']}</h3>"
            f"<p><strong>Release:</strong> {det['release_date']}</p>"
            f"<p><strong>⭐ Rating:</strong> {det['rating']}/10</p>"
            f"<p>{det['overview']}</p>"
            "</div>", unsafe_allow_html=True
        )
    if st.button("🎯 Get Recommendations"):
        ids = recommend_ids(st.session_state.selected, n=t)
        if ids:
            recs = [fetch_movie_details(mid) for mid in ids]
            st.markdown(f"## 🎭 Movies Similar to '{det['title']}'")
            cols = st.columns(5, gap='large')
            for idx, mv in enumerate(recs):
                col = cols[idx % 5]
                with col:
                    st.markdown(
                        f"<div class='movie-card'>"
                        f"<img src='{mv['poster_url']}'/>"
                        f"<h4>{mv['title']} ({mv['release_date'][:4]})</h4>"
                        f"<p>⭐ {mv['rating']}/10</p>"
                        "</div>", unsafe_allow_html=True
                    )
        else:
            st.error("No recommendations available.")
else:
    # Welcome screen
    st.markdown(
        """
        <div style='max-width:800px; margin:50px auto; padding:40px;
                    background: rgba(0,0,0,0.8); border-left: 6px solid #ffcc00;
                    border-radius:15px; box-shadow: 0 4px 20px rgba(0,0,0,0.7);'>
          <h2 style='color:#ffcc00; margin-bottom:10px;'>🍿 Welcome to MovieMine!</h2>
          <p style='color:#e0e0e0; font-size:1.1rem; line-height:1.6;'>
            Discover your next favorite film in seconds. Use the sidebar to search by title or browse the entire catalog.
            Pick any movie you love, and our recommender engine will suggest hidden gems just for you.
          </p>
          <ul style='color:#e0e0e0; font-size:1rem; margin-top:20px;'>
            <li><strong>🔍 Smart Search:</strong> Fuzzy matching finds movies even if you type roughly.</li>
            <li><strong>📋 Complete Catalog:</strong> Browse our entire movie database with ease.</li>
            <li><strong>🎯 Tailored Picks:</strong> Get personalized recommendations based on your selection.</li>
          </ul>
          <p style='text-align:center; margin-top:30px; color:#ffcc00; font-style:italic;'>
            Dig up hidden cinematic gems.
          </p>
        </div>
        """,
        unsafe_allow_html=True
    )
# --- FOOTER ---
st.markdown(
    """
    <div style='max-width:800px; margin:30px auto; padding:20px;
                background: rgba(0,0,0,0.8); border-top: 4px solid #ffcc00;
                border-radius:10px; text-align:center; box-shadow: 0 2px 10px rgba(0,0,0,0.5);'>
      <p style='color:#ffcc00; font-weight:600; margin:0; font-size:1rem;'>
        MovieMine | Powered by TMDb API
      </p>
      <p style='color:#e0e0e0; margin:5px 0 0; font-size:0.9rem;'>
        Enjoy discovering movies tailored to your taste!
      </p>
    </div>
    """,
    unsafe_allow_html=True
)