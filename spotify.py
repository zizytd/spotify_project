import os
import json
import requests
from requests.adapters import HTTPAdapter
from time import sleep
import warnings

warnings.filterwarnings("ignore")

session = requests.Session()
session.mount("http://", HTTPAdapter(max_retries=5))
session.mount("https://", HTTPAdapter(max_retries=5))


def return_access_token(client_id: str, client_secret: str, refresh_token: str):
    headers_token = {
        "Authorization": requests.auth._basic_auth_str(client_id, client_secret),
        "Content-Type": "application/x-www-form-urlencoded",
    }
    token_url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    response = session.post(token_url, data=data, headers=headers_token)
    return response.json()["access_token"]


def last_played_50(limit: int, headers: dict):
    params = {"limit": limit}
    last_played = session.get(
        "https://api.spotify.com/v1/me/player/recently-played",
        headers=headers,
        params=params,
    )
    tracks = last_played.json()["items"]
    tracks_items = [
        [
            track["track"]["id"],
            track["track"]["name"],
            track["track"]["external_urls"]["spotify"],
            track["track"]["preview_url"] if track["track"]["preview_url"] else "",
            str([artist.get("id") for artist in track["track"]["artists"]]),
            track["played_at"],
            track["track"]["duration_ms"],
            [artist.get("id") for artist in track["track"]["artists"]],
        ]
        for track in tracks
    ]
    artists_ids = list(
        set([artist_id for track_item in tracks_items for artist_id in track_item[-1]])
    )
    return [[tuple(track_item[:-1]) for track_item in tracks_items], artists_ids]


def get_artists_ids_details(artists_ids: list, chunksize: int, headers: dict):
    artists_items = []
    for i in range(0, len(artists_ids), chunksize):
        artists_ids_chunk = ",".join(artists_ids[i : i + chunksize])
        params_ids = {"ids": artists_ids_chunk}
        artists = session.get(
            "https://api.spotify.com/v1/artists", headers=headers, params=params_ids
        )
        artists_res = artists.json()
        artists_items.append(
            [
                [
                    i["id"],
                    i["name"],
                    json.dumps((i["genres"])),
                    i["followers"]["total"],
                    i["images"][-1]["url"] if i["images"] else "",
                ]
                for i in artists_res["artists"]
            ]
        )
        sleep(2)
    return [
        tuple(artist_item)
        for artists_item in artists_items
        for artist_item in artists_item
    ]
