
import sqlite3
import libsql_experimental as libsql
import streamlit as st

@st.cache_resource(ttl=3600)
def connection():
    conn = None
    for attempt in range(3):
        try:
            conn = libsql.connect(
                st.secrets["turso"]["turso_db"],
                sync_url=st.secrets["turso"]["turso_db_url"],
                auth_token=st.secrets["turso"]["turso_auth_token"],
            )
            conn.sync()
            if conn:
                break  # Exit the loop if connection is successful
        except Exception as e:
            continue
    if not conn:
        st.error("Failed to connect after 3 attempts.")
    return conn

def get_active_connection():
    try:
        conn = connection() # Your connection function
        cursor = conn.cursor()
        cursor.execute("SELECT 1")  # Simple query to verify connection
    except (sqlite3.OperationalError, sqlite3.DatabaseError, sqlite3.InterfaceError) as e:
        st.cache_resource.clear()  # Clear cache on failure
        conn = connection()  # Retry connection
    return conn
