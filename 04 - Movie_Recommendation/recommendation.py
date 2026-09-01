import pickle



with open(
    "./models/movies.pkl",
    "rb"
) as file:

    movies = pickle.load(file)



# with open(
#     "./models/tfidf_vectorizer.pkl",
#     "rb"
# ) as file:

#     tfidf = pickle.load(file)



with open(
    "./models/similarity_matrix.pkl",
    "rb"
) as file:

    similarity_matrix = pickle.load(file)





# Recommendation function

def recommend_movies(movie_title, n=5):

    if not isinstance(movie_title, str):
        return []

    if not isinstance(n, int) or n <= 0:
        return []

    movie_title = movie_title.strip().lower()

    matches = movies[
        movies["normalized_title"] == movie_title
    ]

    if matches.empty:
        return []

    movie_index = matches.index[0]

    similarity_scores = similarity_matrix[
        movie_index
    ]

    sorted_movies = sorted(
        list(enumerate(similarity_scores)),
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for index, score in sorted_movies[1:n + 1]:

        recommendations.append({
            "id": int(movies.iloc[index]["id"]),
            "title": movies.iloc[index]["original_title"],
            "score": float(
                similarity_scores[index]
            )
        })

    return recommendations

