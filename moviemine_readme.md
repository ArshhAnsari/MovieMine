# MovieMine 🎬

**A Smart Movie Recommendation System powered by Machine Learning and TMDb API**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://moviemine-pvt-stream.streamlit.app/)

## 🎯 Project Overview

MovieMine is an intelligent movie recommendation system that leverages content-based filtering and machine learning to suggest personalized movie recommendations. Built with Streamlit for an interactive web interface, the application combines the power of cosine similarity algorithms with real-time movie data from The Movie Database (TMDb) API to deliver accurate and relevant movie suggestions.

## 🚀 Live Demo

**🔗 [Try MovieMine Live](https://moviemine-pvt-stream.streamlit.app/)**

Experience the full functionality of MovieMine with our deployed application!

## ✨ Key Features

### 🔍 **Smart Search Engine**
- **Fuzzy String Matching**: Advanced search using FuzzyWuzzy library that finds movies even with typos or partial titles
- **Real-time Search Results**: Instant suggestions as you type with confidence scores
- **Flexible Input**: Handles variations in movie titles and common misspellings

### 🎭 **Intelligent Recommendations**
- **Content-Based Filtering**: Uses movie features like genres, cast, crew, and keywords
- **Cosine Similarity Algorithm**: Mathematical approach to find movies with similar characteristics
- **Customizable Results**: Adjustable recommendation count (5-20 movies)
- **High Accuracy**: Pre-computed similarity matrix for fast and accurate suggestions

### 🎨 **Modern User Interface**
- **Responsive Design**: Optimized for desktop and mobile devices
- **Dark Theme**: Cinema-inspired color scheme with golden accents
- **Interactive Cards**: Hover effects and smooth transitions
- **Custom Styling**: CSS-enhanced components for better user experience

### 📊 **Rich Movie Information**
- **TMDb Integration**: Real-time movie details, ratings, and high-quality posters
- **Comprehensive Details**: Release dates, ratings, overviews, and poster images
- **Visual Presentation**: Card-based layout for easy browsing

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MovieMine Architecture                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │   Streamlit     │    │   TMDb API      │                 │
│  │   Frontend      │◄──►│   Integration   │                 │
│  └─────────────────┘    └─────────────────┘                 │
│           │                       │                         │
│           ▼                       ▼                         │
│  ┌─────────────────┐    ┌─────────────────┐                 │
│  │   Search        │    │   Movie Details │                 │
│  │   Engine        │    │   Fetcher       │                 │
│  │  (FuzzyWuzzy)   │    │                 │                 │
│  └─────────────────┘    └─────────────────┘                 │
│           │                       │                         │
│           ▼                       ▼                         │
│  ┌─────────────────────────────────────────┐                │
│  │          Core Recommendation            │                │
│  │               Engine                    │                │
│  │                                         │                │
│  │  ┌─────────────┐  ┌─────────────────┐   │                │
│  │  │   Movie     │  │   Similarity    │   │                │
│  │  │ Database    │  │    Matrix       │   │                │
│  │  │ (Pickle)    │  │   (Pickle)      │   │                │
│  │  └─────────────┘  └─────────────────┘   │                │
│  └─────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### 🔧 **Core Components**

#### 1. **Data Layer**
- **movie_dict.pkl**: Serialized pandas DataFrame containing movie metadata
- **similarity.pkl**: Pre-computed cosine similarity matrix for all movies
- **Efficient Storage**: Pickle format for fast loading and minimal memory usage

#### 2. **API Integration Layer**
- **TMDb API Client**: Fetches real-time movie details, ratings, and poster images
- **Error Handling**: Robust exception handling for API failures
- **Rate Limiting**: Efficient API usage to prevent quota exhaustion

#### 3. **Search Engine**
- **FuzzyWuzzy Integration**: Partial ratio scoring for flexible search
- **Configurable Threshold**: 60% minimum similarity for relevant results
- **Performance Optimized**: Fast string matching algorithms

#### 4. **Recommendation Engine**
- **Content-Based Filtering**: Analyzes movie features for similarity
- **Cosine Similarity**: Mathematical approach using feature vectors
- **Scalable Algorithm**: Handles large movie databases efficiently

#### 5. **Frontend Layer**
- **Streamlit Framework**: Interactive web application
- **Responsive Design**: CSS Grid and Flexbox for layout
- **State Management**: Session state for user interactions

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Web application framework |
| **Backend** | Python | Core application logic |
| **ML Algorithm** | Cosine Similarity | Recommendation engine |
| **Search** | FuzzyWuzzy | Fuzzy string matching |
| **API** | TMDb API | Movie data and images |
| **Data Storage** | Pickle | Serialized data storage |
| **Styling** | CSS3 | Custom UI components |
| **Data Processing** | Pandas | Data manipulation |
| **HTTP Requests** | Requests | API communication |

## 📁 Project Structure

```
MovieMine/
├── app.py                 # Main Streamlit application
├── movie_dict.pkl         # Movie database (DataFrame)
├── similarity.pkl         # Similarity matrix
├── .streamlit/
│   └── secrets.toml      # API keys and configuration
├── pics/
│   └── bg.jpg           # Background image (optional)
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🔄 Algorithm Deep Dive

### **Content-Based Filtering Process**

1. **Feature Engineering**
   ```python
   # Movie features typically include:
   - Genres (Action, Comedy, Drama, etc.)
   - Cast members (Top actors)
   - Crew (Director, Producer)
   - Keywords (Plot-related terms)
   - Production companies
   ```

2. **Vectorization**
   ```python
   # Convert text features to numerical vectors
   from sklearn.feature_extraction.text import TfidfVectorizer
   
   # Create TF-IDF vectors for movie features
   tfidf = TfidfVectorizer(stop_words='english')
   feature_matrix = tfidf.fit_transform(movie_features)
   ```

3. **Similarity Calculation**
   ```python
   # Compute cosine similarity matrix
   from sklearn.metrics.pairwise import cosine_similarity
   
   similarity_matrix = cosine_similarity(feature_matrix)
   ```

4. **Recommendation Generation**
   ```python
   def recommend_movies(movie_index, similarity_matrix, n=10):
       # Get similarity scores for selected movie
       sim_scores = list(enumerate(similarity_matrix[movie_index]))
       
       # Sort by similarity score
       sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
       
       # Return top N similar movies (excluding the input movie)
       return sim_scores[1:n+1]
   ```

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.7 or higher
- TMDb API key (free registration required)

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/ArshhAnsari/MovieMine.git
cd MovieMine
```

### **Step 2: Install Dependencies**
```bash
pip install streamlit pandas requests fuzzywuzzy python-levenshtein
```

### **Step 3: Configure API Key**
1. Create a `.streamlit` folder in the project root:
   ```bash
   mkdir .streamlit
   ```

2. Create `secrets.toml` file inside `.streamlit` folder:
   ```bash
   touch .streamlit/secrets.toml
   ```

3. Add your TMDb API key to `secrets.toml`:
   ```toml
   # .streamlit/secrets.toml
   tmdb_token = "your_tmdb_api_key_here"
   ```

### **Step 4: Get TMDb API Key**
1. Visit [The Movie Database](https://www.themoviedb.org/)
2. Create a free account
3. Go to Settings → API
4. Request an API key
5. Copy the API key to your `secrets.toml` file

### **Step 5: Run the Application**
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 🎮 Usage Guide

### **1. Search for Movies**
- Use the sidebar search box to find movies by title
- The fuzzy search will show matches even with partial or misspelled names
- Each result shows a confidence percentage

### **2. Browse Movies**
- Use the dropdown menu to browse all available movies
- Scroll through the complete catalog alphabetically

### **3. Get Recommendations**
- Select any movie from search results or dropdown
- Adjust the number of recommendations using the slider (5-20)
- Click "Get Recommendations" to see similar movies

### **4. View Movie Details**
- Selected movies display with poster, rating, release date, and overview
- Recommended movies show in a responsive card layout
- All data is fetched in real-time from TMDb


## 🙏 Acknowledgements

* **TMDb** – For providing movie data and posters via their API.

  > *“This product uses the TMDb API but is not endorsed or certified by TMDb.”*

* **Streamlit Cloud** – For hosting and deploying the app effortlessly.

## 🤝 Contributing

Contributions are welcome!

- **Live Demo**: [MovieMine Application](https://moviemine-pvt-stream.streamlit.app/)
- **Issues**: Please report bugs and feature requests via GitHub Issues

---

**⭐ If you found this project helpful, please consider giving it a star!**

*Dig up hidden cinematic gems with MovieMine* 🎬✨