import os
from time import sleep
import warnings
import libsql_experimental as libsql
from spotify import *

warnings.filterwarnings("ignore")

access_token = return_access_token(
    os.getenv("client_id_spotify"),
    os.getenv("client_secret_spotify"),
    os.getenv("refresh_token"),
)
headers = {"Authorization": f"Bearer {access_token}"}

tracks_items, artists_ids = last_played_50(50, headers)

artists_details = get_artists_ids_details(artists_ids, 50, headers)


conn = libsql.connect(
    os.getenv("turso_db"),
    sync_url=os.getenv("turso_db_url"),
    auth_token=os.getenv("turso_auth_token"),
)
conn.sync()

previous_listened_spotify = "previous_listened_spotify_tracks_table"
artists_listened = "artists_listened_table"
primary_key_listened = "(id, played_at)"
primary_key_artist = "(id)"
previous_listened_spotify_column = f"id TEXT,name TEXT,track_url TEXT,track_preview_url TEXT,artists_ids TEXT,played_at TEXT,duration_ms INTEGER,PRIMARY KEY {primary_key_listened}"
artists_listened_column = f"id TEXT,name TEXT,genres TEXT,followers INTEGER,image_url TEXT,PRIMARY KEY {primary_key_artist}"


def load_data_2_db(
    table_name: str,
    table_columns: str,
    data: list,
    primary_key: str,
    conflict="NOTHING",
):
    conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({table_columns})")
    exe_many = f"INSERT INTO {table_name} VALUES ({', '.join('?'*len(data[0]))}) ON CONFLICT {primary_key} DO {conflict}"
    if conflict == "UPDATE SET":
        combined_str = ", ".join(
            [
                f"{i.split()[0]} = excluded.{i.split()[0]}"
                for i in table_columns.split(",")
            ][1:-2]
        )
        exe_many = f"INSERT INTO {table_name} VALUES ({', '.join('?'*len(data[0]))}) ON CONFLICT{primary_key} DO {conflict} {combined_str}"
    chunksize = 20
    attempt = 3
    for h in range(attempt):
        try:
            for i in range(0, len(data), chunksize):
                conn.executemany(
                    exe_many,
                    data[i : i + chunksize],
                )
                conn.commit()
                break
        except ValueError:
            if h < attempt - 1:
                print(f"Transaction timed out. Retrying.")
                sleep(5)
            else:
                raise


load_data_2_db(
    previous_listened_spotify,
    previous_listened_spotify_column,
    tracks_items,
    primary_key_listened,
)
sleep(2)
load_data_2_db(
    artists_listened,
    artists_listened_column,
    artists_details,
    primary_key_artist,
    "UPDATE SET",
)