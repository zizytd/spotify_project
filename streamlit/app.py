import streamlit as st

st.set_page_config(page_icon="🎶", layout="wide")

st.logo("streamlit/images/spotify.jpg")

home_page = st.Page("app_pages/home.py", title="Home", icon="🏠")
track_page = st.Page("app_pages/top_listened.py", title="Top Tracks", icon="🎵")
artist_page = st.Page("app_pages/artist.py", title="Top Artists", icon="🎸")

pg = st.navigation([home_page, track_page, artist_page])
pg.run()
