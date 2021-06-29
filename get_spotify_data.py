from requests.models import HTTPError
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET= os.getenv('CLIENT_SECERET')

auth_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)



spot = spotipy.Spotify(auth_manager=auth_manager)

def get_songs_in_playlist(user, playlist_uri):
    '''
    Returns a list of songs from the specified playlist URI.
    
    :param playlist_uri: The Spotify playlist URL. 
    
    :returns: A dict of song objects. 
    '''
    
    tracks = 'tracks'
    track = 'track'
    items = 'items'
    name = 'name'
    artists = 'artists'
    
    playlist_songs = {}
    playlist = spot.user_playlist(user, playlist_uri)
    playlist_name = playlist['name']

    for item in playlist[tracks][items]:
        title = item[track][name]
        artist = item[track][artists][0][name]
        playlist_songs[title] = artist

    print(f"Playlist {playlist_name} songs: {playlist_songs}")
    return playlist_songs
        
