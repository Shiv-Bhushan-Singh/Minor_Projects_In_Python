import os

import requests
import streamlit as st
from dotenv import load_dotenv




load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("BOOK_API_KEY")

if not GOOGLE_BOOKS_API_KEY:
    st.error("Google Books API key is missing.")
    st.stop()



BASE_URL = "https://www.googleapis.com/books/v1/volumes"



# Google Books API


@st.cache_data(ttl=600)
def search_books(query: str, max_results: int = 10):

    params = {
        "q": query,
        "maxResults": max_results,
        "key": GOOGLE_BOOKS_API_KEY
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        st.error("The Google Books API request timed out.")
        return None

    except requests.exceptions.HTTPError as error:

        if response.status_code == 429:
            st.error(
                "Too many requests. Please wait a moment and try again."
            )

        elif response.status_code == 401:
            st.error(
                "Invalid Google Books API key."
            )

        else:
            st.error(
                f"Google Books API error: {response.status_code}"
            )

        return None

    except requests.exceptions.RequestException as error:
        st.error(
            f"Unable to connect to Google Books API: {error}"
        )
        return None



st.set_page_config(
    page_title="Book Finder",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Book Finder")

st.write(
    "Search for books using the Google Books API."
)


# Search input


query = st.text_input(
    "Search for a book",
    placeholder="e.g. Harry Potter, Atomic Habits, The Alchemist"
)



# Search button


if st.button("Search", type="primary"):

    if not query.strip():

        st.warning("Please enter a book title or keyword.")

    else:

        with st.spinner("Searching books..."):

            data = search_books(
                query=query.strip(),
                max_results=10
            )

        if data is None:
            st.stop()

        total_items = data.get("totalItems", 0)

        if total_items == 0:

            st.info("No books found.")

        else:

            books = data.get("items", [])

            st.success(
                f"Found books."
            )

            # Display books

            for book in books:

                volume_info = book.get(
                    "volumeInfo",
                    {}
                )

                title = volume_info.get(
                    "title",
                    "Unknown Title"
                )

                authors = volume_info.get(
                    "authors",
                    ["Unknown Author"]
                )

                description = volume_info.get(
                    "description",
                    "No description available."
                )

                categories = volume_info.get(
                    "categories",
                    ["Unknown"]
                )

                published_date = volume_info.get(
                    "publishedDate",
                    "Unknown"
                )

                page_count = volume_info.get(
                    "pageCount",
                    "Unknown"
                )

                rating = volume_info.get(
                    "averageRating",
                    "Not rated"
                )

                image_links = volume_info.get(
                    "imageLinks",
                    {}
                )

                thumbnail = image_links.get(
                    "thumbnail"
                )

                info_link = volume_info.get(
                    "infoLink"
                )


                # --------------------------------------------------
                # Book card
                # --------------------------------------------------

                with st.container(border=True):

                    col1, col2 = st.columns(
                        [1, 4]
                    )

                    with col1:

                        if thumbnail:

                            st.image(
                                thumbnail,
                                width=130
                            )

                        else:

                            st.write(
                                "📕 No cover"
                            )


                    with col2:

                        st.subheader(title)

                        st.write(
                            f"**Author:** {', '.join(authors)}"
                        )

                        st.write(
                            f"**Published:** {published_date}"
                        )

                        st.write(
                            f"**Pages:** {page_count}"
                        )

                        st.write(
                            f"**Rating:** ⭐ {rating}"
                        )

                        st.write(
                            f"**Category:** {', '.join(categories)}"
                        )

                        st.write(
                            description
                        )

                        if info_link:

                            st.link_button(
                                "View Book",
                                info_link
                            )