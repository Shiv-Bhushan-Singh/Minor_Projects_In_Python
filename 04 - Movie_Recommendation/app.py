import streamlit as st

from recommendation import (
    movies,
    recommend_movies
)

from services.tmdb_service import (
    get_movie_details,
    get_poster_url
)



st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)



@st.cache_data(ttl=3600)
def fetch_movie_details(movie_id):

    return get_movie_details(
        movie_id
    )


st.title(
    "🎬 Movie Recommendation System"
)

st.write(
    "Discover movies similar to your favorite "
    "movies using content-based machine learning."
)


movie_titles = (
    movies["original_title"]
    .dropna()
    .drop_duplicates()
    .sort_values()
    .tolist()
)



movie_title = st.selectbox(
    "Choose a movie",
    movie_titles
)



number_of_movies = st.slider(
    "Number of recommendations",
    min_value=1,
    max_value=10,
    value=5
)


if st.button(
    "🎬 Recommend Movies",
    use_container_width=True
):

    recommendations = recommend_movies(
        movie_title,
        n=number_of_movies
    )


    if not recommendations:

        st.warning(
            "No recommendations found."
        )

    else:

        st.subheader(
            f"Movies similar to {movie_title}"
        )


        columns = st.columns(
            len(recommendations)
        )


        for column, movie in zip(
            columns,
            recommendations
        ):

            with column:

                movie_data = fetch_movie_details(
                    movie["id"]
                )


                # if movie_data is None:

                #     st.error(
                #         f"Unable to load "
                #         f"{movie['title']}"
                #     )

                #     continue
                
                if movie_data is None:

                    st.markdown(
                        f"### {movie['title']}"
                    )
                
                    st.write(
                        f"🤖 Similarity: "
                        f"**{movie['score']:.1%}**"
                    )
                
                    st.warning(
                        "Information unavailable."
                    )
                
                    continue


                poster_url = get_poster_url(
                    movie_data["poster_path"]
                )



                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "Poster unavailable"
                    )


                st.markdown(
                    f"### {movie['title']}"
                )

                st.write(
                    f"🤖 Similarity: "
                    f"**{movie['score']:.1%}**"
                )


                rating = movie_data.get(
                    "rating"
                )

                if rating is not None:

                    st.write(
                        f"⭐ TMDB Rating: "
                        f"**{rating:.1f}/10**"
                    )


                release_date = (
                    movie_data.get(
                        "release_date"
                    )
                )

                if release_date:

                    st.write(
                        f"📅 {release_date}"
                    )


                overview = (
                    movie_data.get(
                        "overview"
                    )
                )

                if overview:

                    st.write(
                        overview
                    )



st.divider()
