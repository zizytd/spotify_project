import streamlit as st
import pandas as pd
import altair as alt
from database import get_active_connection
from st_social_media_links import SocialMediaIcons
import warnings

warnings.filterwarnings('ignore')


st.header("My Spotify Vibes 😎")
social_media_links = [
            "https://www.linkedin.com/in/tochukwu-onyido-97b07591/",
            "https://github.com/zizytd"]

social_media_icons = SocialMediaIcons(social_media_links) 
social_media_icons.render(sidebar=True, justify_content="center")

with st.expander("About This App"):
    st.markdown("""This app displays the aggregated data of my Spotify listening patterns starting from August 2024, sourced from an ETL pipeline. 
The pipeline extracts data from the [Spotify API](https://developer.spotify.com/documentation/web-api) and loads 
                it into an SQLite database hosted on the [Turso platform](https://docs.turso.tech/introduction), with the entire ETL process automated through GitHub Actions.

The App Pages details are as follows: 

- Home Page – A high-level overview of various statistics based on listening data.
- Track Page – Displays most-played tracks, with a default view of the top 10. You can adjust the number of tracks shown using the slider in the sidebar.
- Artist Page – Shows most-listened-to artists, with a default display of the top 10. The count can be increased or decreased using the sidebar slider.""")

st.markdown('<br>',unsafe_allow_html=True)

conn = get_active_connection()

def generate_html(query_path):
    with open(query_path) as q:
        query = q.read()
    
    st.cache_data(ttl=3600, show_spinner="Fetching data from Database....")
    def query_data():
        return pd.read_sql(query, conn)

    try:
        df = query_data()
    except Exception as e:
        st.error(e)
        st.stop()

    values_details  = df.values.tolist()

    html_table = f"""<table>
    <thead style="background-color:#3ce860">
    <tr>
        <th>{df.columns[0]}</th>
        <th>{df.columns[1]}</th>
    </tr>
    </thead>
    <tbody>
    """
    part_body = ""
    for val in values_details:
        part_body += f"""<tr><td>{val[0]}</td><td>{val[1]}</td></tr>"""

    html_table = html_table + part_body + """</tbody>
                                            </table>
                                            """
    return html_table,df

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Total Summary**")
        html_table = generate_html("streamlit/queries/summary.txt")[0]
        st.markdown(html_table,unsafe_allow_html=True)
    with col2:
        st.write("**Top 5 Genres**")
        html_table = generate_html("streamlit/queries/top_genres.txt")[0]
        st.markdown(html_table,unsafe_allow_html=True)

    st.markdown("<hr>",unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        df = generate_html("streamlit/queries/top_dates.txt")[1]
        bar = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X("Date", axis=alt.Axis(labelAngle=360)),
                y="Count",
            )
        )

        # Define the text chart
        text = (
            alt.Chart(df)
            .mark_text(align="center", dy=6, color="white")
            .encode(
                x=alt.X("Date", axis=alt.Axis(labelAngle=360)),
                y="Count",
                text="Count",
            )
        )

        # Combine the charts into a layer chart
        acc_alt = (
            alt.layer(bar, text)
            .configure_mark(color="#3ce860")
            .interactive()
            .properties(
                title={
                    "text": "Top 5 Dates by Number of Listens",
                    "anchor": "middle",
                    "align": "center",
                }
            )
        )
        st.altair_chart(acc_alt, theme="streamlit", use_container_width=True)
    with col4:
        df = generate_html("streamlit/queries/last_seven.txt")[1]
        df_alt_line = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x=alt.X("Date", axis=alt.Axis(labelAngle=360)),
                y="Count",
            )
            .interactive()
            .configure_mark(color="#3ce860")
            .properties(
                title={
                    "text": "Last Seven Days Listening Count",
                    "anchor": "middle",
                    "align": "center",
                }
            )
        )
        st.altair_chart(df_alt_line, theme="streamlit", use_container_width=True)
