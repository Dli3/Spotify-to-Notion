from notion import Notion
from get_spotify_data import get_songs_in_playlist
import sys

def main():
    notion = Notion()
    songs = get_songs_in_playlist('my_user', sys.argv[1])

    for title, author in songs.items():
        print(f'{title} - {author}')
        notion.create_page(title, author)
    
if __name__=='__main__':
    try:
        if sys.argv[1]:
            main()
    except IndexError:
        print("Please specify the Spotify playlist's URI")
