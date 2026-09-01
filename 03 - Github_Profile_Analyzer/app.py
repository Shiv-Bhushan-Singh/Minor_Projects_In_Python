import streamlit as st
import pandas as pd
import plotly.express as px
import requests

from github_service import (
    get_profile,
    get_repositories
)


st.set_page_config(
    page_title="GitHub Profile Analyzer",
    page_icon="🧑‍💻",
    layout="wide"
)




@st.cache_data(ttl=600)
def fetch_profile(username):

    return get_profile(username)


@st.cache_data(ttl=600)
def fetch_repositories(username):

    return get_repositories(username)



st.title(
    "🧑‍💻 GitHub Profile Analyzer"
)

st.write(
    "Analyze a GitHub profile using the GitHub REST API."
)



username = st.text_input(
    "Enter GitHub username",
    placeholder="e.g. octocat"
)




if st.button(
    "🔍 Analyze Profile",
    use_container_width=True
):

    if not username.strip():

        st.warning(
            "Please enter a GitHub username."
        )

        st.stop()


    username = username.strip()


    try:

        profile = fetch_profile(
            username
        )

        repositories = fetch_repositories(
            username
        )


    except requests.RequestException:

        st.error(
            "Unable to connect to GitHub."
        )

        st.stop()


    if profile is None:

        st.error(
            f"GitHub user '{username}' was not found."
        )

        st.stop()


    if repositories is None:

        st.error(
            "Unable to retrieve repositories."
        )

        st.stop()



    col1, col2 = st.columns(
        [1, 3]
    )


    with col1:

        if profile.get("avatar_url"):

            st.image(
                profile["avatar_url"],
                use_container_width=True
            )


    with col2:

        st.header(
            profile.get(
                "name"
            ) or profile["login"]
        )

        st.write(
            f"@{profile['login']}"
        )

        if profile.get("bio"):

            st.write(
                profile["bio"]
            )

        if profile.get("html_url"):

            st.link_button(
                "View GitHub Profile",
                profile["html_url"]
            )


    st.divider()

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Followers",
        profile.get(
            "followers",
            0
        )
    )


    col2.metric(
        "Following",
        profile.get(
            "following",
            0
        )
    )


    col3.metric(
        "Public Repositories",
        profile.get(
            "public_repos",
            0
        )
    )


    col4.metric(
        "Public Gists",
        profile.get(
            "public_gists",
            0
        )
    )



    if not repositories:

        st.info(
            "This user has no public repositories."
        )

        st.stop()


    repo_data = []


    for repo in repositories:

        repo_data.append({

            "Name": repo.get(
                "name"
            ),

            "Language": repo.get(
                "language"
            ) or "Unknown",

            "Stars": repo.get(
                "stargazers_count",
                0
            ),

            "Forks": repo.get(
                "forks_count",
                0
            ),

            "Open Issues": repo.get(
                "open_issues_count",
                0
            ),

            "Updated": repo.get(
                "updated_at"
            ),

            "URL": repo.get(
                "html_url"
            )
        })


    df = pd.DataFrame(
        repo_data
    )



    st.subheader(
        "📊 Repository Statistics"
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Total Stars",
        int(df["Stars"].sum())
    )


    col2.metric(
        "Total Forks",
        int(df["Forks"].sum())
    )


    col3.metric(
        "Total Open Issues",
        int(df["Open Issues"].sum())
    )


    language_counts = (
        df["Language"]
        .value_counts()
        .reset_index()
    )


    language_counts.columns = [
        "Language",
        "Repositories"
    ]


    st.subheader(
        "💻 Programming Languages"
    )


    fig = px.pie(
        language_counts,
        names="Language",
        values="Repositories",
        title="Repository Language Distribution"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )




    st.subheader(
        "⭐ Top Repositories"
    )


    top_repositories = (
        df.sort_values(
            "Stars",
            ascending=False
        )
        .head(10)
    )


    st.dataframe(
        top_repositories[
            [
                "Name",
                "Language",
                "Stars",
                "Forks",
                "Open Issues"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )



    st.subheader(
        "📚 Repositories"
    )


    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "URL": st.column_config.LinkColumn(
                "Repository"
            )
        }
    )



    if len(repositories) == 100:

        st.info(
            "Showing up to 100 repositories."
        )