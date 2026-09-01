import os
import pickle

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


os.makedirs("models", exist_ok=True)

movies = pd.read_csv(
    "./data/featured_movie.csv"
)

movies["tags"] = movies["tags"].fillna("")

movies["normalized_title"] = (
    movies["original_title"]
    .str.strip()
    .str.lower()
)


tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

tfidf_matrix = tfidf.fit_transform(
    movies["tags"]
)

similarity_matrix = cosine_similarity(
    tfidf_matrix
)


with open(
    "./models/tfidf_vectorizer.pkl",
    "wb"
) as file:

    pickle.dump(
        tfidf,
        file
    )
    
    
    
with open(
    "./models/similarity_matrix.pkl",
    "wb"
) as file:

    pickle.dump(
        similarity_matrix,
        file
    )
    
    
with open(
    "./models/movies.pkl",
    "wb"
) as file:

    pickle.dump(
        movies,
        file
    )
    
    
print("TF-IDF matrix shape:", tfidf_matrix.shape)
print(
    "Similarity matrix shape:",
    similarity_matrix.shape
)
print("Model artifacts saved successfully.")