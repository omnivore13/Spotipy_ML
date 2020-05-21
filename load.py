"""Extracts Song Features from Spotify using Spotipy"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json


def chunks(l, n):
    for i in range(0, len(l), n):
        yield list(l[i:i + n])


secret = """Your Client Secret Key Here"""
cid = """Your Client ID Here"""
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False
tracks = sp.user_playlist("217nkz5ceb65yipbxwbiacmeq", "3fwMqnOaHI3iOCjtbPkHnZ")
songs = tracks['tracks']['items']
ids = [song['track']['id'] for song in songs]
track_details = []
mytracks = chunks(ids, 50)
for chunk in mytracks:
    track_chunk = (sp.tracks(tracks=ids[:50]))
    for track in track_chunk['tracks']:
        track_details.append([track['id'], track['name'], track['artists'][0]['name']])
features = sp.audio_features(ids)
features = pd.DataFrame(features)
td = pd.DataFrame(track_details)
td.rename(columns={0: 'id', 1: 'Track Name', 2: 'Lead Artist'}, inplace=True)
df = (pd.merge(features, td))
df.index = df['id']
df.drop(['uri','track_href','analysis_url','id', 'time_signature'], axis=1, inplace=True)
df.to_csv('mydata.csv')
