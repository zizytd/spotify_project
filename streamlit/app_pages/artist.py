import streamlit as st
import pandas as pd
from database import get_active_connection
import warnings

warnings.filterwarnings('ignore')


with open("streamlit/queries/top_listened_artists.txt") as q:
    query = q.read()


num = st.sidebar.slider("Select Limit",min_value=5,value=10,step=5,max_value=20,key='num_count')

st.header(f"Top {st.session_state.num_count} Most Played Artists 💃🏽 🕺")

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

# Create HTML table with embedded CSS for styling
html_table = """
<style>
    .scrollable-table {
        max-height: 900px;
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
        background-color: #3ce860;  /* Set the custom background color */
        color: white;  /* Make the header text white for contrast */
        position: sticky;  /* Sticky header */
        top: 0;          /* Stick to the top */
        z-index: 1;     /* Ensure it appears above the content */
    }
    tbody tr {
        height: 100px; /* Set row height */
    }
    td {
        text-align: center;
        border-bottom: 1px solid #ddd;
        word-wrap: break-word;  /* Wrap text within cells */
        height: 100px; /* Set the same height for cells as rows */
        line-height: 100px; /* Center text vertically within the cell */
        padding: 0; /* Remove padding to keep height consistent */
    }
    td img {
        max-height: 120%; /* Ensure images fit within the cell height */
        width: 100px; /* Auto width to maintain aspect ratio */
        height: 100px;
    }
    td.count-cell {
        width: 200px;  /* Explicitly set width for count column */
    }
</style>

<div class="scrollable-table">
<table>
    <thead>
    <tr>
        <th>Artist Name</th>
        <th>Artist Followers Count</th>
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
                        <td><img src="{val[2]}" alt="{val[0]}"></td>
                        <td class="count-cell">{val[3]}</td>
                     </tr>"""

html_table += part_body + """</tbody>
                                        </table>
                                        </div>"""

# Render the HTML table in Streamlit
st.markdown(html_table, unsafe_allow_html=True)