import streamlit as st
import pandas as pd
from database import get_active_connection
import warnings

warnings.filterwarnings("ignore")


with open("streamlit/queries/top_listened.txt") as q:
    query = q.read()


num = st.sidebar.slider(
    "Select Limit", min_value=5, value=10, step=5, max_value=20, key="num_count"
)

st.header(f"Top {st.session_state.num_count} Most Played Songs 🎧")

conn = get_active_connection()


st.cache_data(ttl=3600, show_spinner="Fetching data from Database....")


def query_data(num):
    return pd.read_sql(query.format(num=num), conn)


try:
    df = query_data(num)
except Exception as e:
    st.error(e)
    st.stop()

values = df.values.tolist()


html_table = """
<style>
    .scrollable-table {
        max-height: 600px;
        overflow-y: auto;
        display: block;
        border: 1px solid #ccc;
        width: 100%;
    }
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th {
        text-align: center;
        padding: 8px;
        background-color: #3ce860;  /* Set the custom background color */
        color: black;  /* Make the header text white for contrast */
        position: sticky;  /* Sticky header */
        top: 0;          /* Stick to the top */
        z-index: 1;     /* Ensure it appears above the content */
    }
    tbody tr {
        height: 50px; /* Set row height to a smaller value */
    }
    td {
        text-align: center;
        padding: 4px; /* Reduce padding to control height */
        border-bottom: 1px solid #ddd;
        word-wrap: break-word;  /* Wrap text within cells */
        max-width: 230px;  /* Control the max width of each column */
        vertical-align: middle; /* Center content vertically */
    }
    td.audio-cell {
        width: 300px;  /* Explicitly set width for audio column */
    }
    audio {
        width: 100%;  /* Ensure the audio player fits within the column */
        max-height: 30px; /* Limit the height of the audio player */
    }
    td img {
        width: 100px; /* Set a fixed width for images */
        height: 100px; /* Set a fixed height for images */
        object-fit: cover; /* Ensure the image covers the area without distortion */
    }
</style>

<div class="scrollable-table">
<table>
    <thead>
    <tr>
        <th>Track Name</th>
        <th>Artist</th>
        <th>URL</th>
        <th>Preview Audio</th>
        <th>Artist Image</th>
        <th>Count</th>
    </tr>
    </thead>
    <tbody>
"""
part_body = ""
for val in values:
    part_body += f"""<tr>
                        <td>{val[0]}</td>
                        <td>{val[1]}</td>
                        <td><a href="{val[2]}" target="_blank">Track URL</a></td>
                        <td class="audio-cell"><audio controls src="{val[3]}"></audio></td>
                        <td><img src="{val[4]}" alt="{val[0]}"></td>
                        <td>{val[5]}</td>
                     </tr>"""

html_table += (
    part_body
    + """</tbody>
                                        </table>
                                        </div>"""
)

# Render the HTML table in Streamlit
st.markdown(html_table, unsafe_allow_html=True)
