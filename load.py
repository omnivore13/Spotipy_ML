"""Extracts Song Features from Spotify using Spotipy"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


client_secret = str(input('Please enter your Client Secret Key: (WARNING: DO NOT SHARE THIS KEY WITH ANYONE!): '))
client_id = str(input("Please Enter your Client ID here: "))
user_id = str(input('Please Enter your User ID Here: '))
playlist_id = str(input('Please Enter Playlist ID to get audio features for all tracks in playlist: '))
def chunks(l, n):
    for i in range(0, len(l), n):
        yield list(l[i:i + n])


client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False
tracks = sp.user_playlist(user=user_id, playlist_id=playlist_id)
songs = tracks['tracks']['items']
ids = [song['track']['id'] for song in songs]
track_details = []
mytracks = chunks(ids, 50)
for chunk in mytracks:
    track_chunk = (sp.tracks(tracks=list(chunk)))
    for track in track_chunk['tracks']:
        track_details.append([track['id'], track['name'], track['artists'][0]['name']])
features = sp.audio_features(ids)
features = pd.DataFrame(features)
td = pd.DataFrame(track_details)
td.rename(columns={0: 'id', 1: 'Track Name', 2: 'Lead Artist'}, inplace=True)
df = (pd.merge(features, td))
df.index = df['id']
df.drop(['uri', 'track_href', 'analysis_url', 'time_signature', 'id', 'type'], axis=1, inplace=True)
df.to_csv('mydata.csv')