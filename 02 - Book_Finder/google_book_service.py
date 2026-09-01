import requests


BASE_URL = (
    "https://www.googleapis.com/books/v1/volumes"
)


# def search_books(
#     query,
#     max_results=10
# ):

#     if not query or not query.strip():
#         return []

#     params = {
#         "q": query.strip(),
#         "maxResults": max_results
#     }

#     try:

#         response = requests.get(
#             BASE_URL,
#             params=params,
#             timeout=10
#         )

#         response.raise_for_status()

#         data = response.json()

#         return data.get(
#             "items",
#             []
#         )

#     except requests.RequestException:

#         return []





def search_books(query, max_results=10):

    if not query or not query.strip():
        return []

    params = {
        "q": query.strip(),
        "maxResults": max_results
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        print("Status code:", response.status_code)
        print("Request URL:", response.url)

        response.raise_for_status()

        data = response.json()

        print("Total items:", data.get("totalItems", 0))

        return data.get("items", [])

    except requests.RequestException as exc:

        print(
            f"Google Books API request failed: {exc}"
        )

        return []






def format_book(item):

    volume_info = item.get(
        "volumeInfo",
        {}
    )

    image_links = volume_info.get(
        "imageLinks",
        {}
    )

    return {
        "id": item.get("id"),
        "title": volume_info.get(
            "title",
            "Unknown title"
        ),
        "authors": volume_info.get(
            "authors",
            []
        ),
        "description": volume_info.get(
            "description",
            ""
        ),
        "publisher": volume_info.get(
            "publisher",
            ""
        ),
        "published_date": volume_info.get(
            "publishedDate",
            ""
        ),
        "categories": volume_info.get(
            "categories",
            []
        ),
        "rating": volume_info.get(
            "averageRating"
        ),
        "ratings_count": volume_info.get(
            "ratingsCount",
            0
        ),
        "page_count": volume_info.get(
            "pageCount"
        ),
        "thumbnail": image_links.get(
            "thumbnail"
        ),
        "info_link": volume_info.get(
            "infoLink"
        )
    }