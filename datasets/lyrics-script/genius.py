import json
import lyricsgenius as lg
import pandas as pd

OUTPUT_FILE_PREFIX = '../'
OUTPUT_FILE_SUFFIX = ' Lyrics.csv'


def read_api_info() -> dict:
    """
    Reads the API information from the file genius-api.json and returns it as a dictionary. The dictionary contains these keys:
    - client_id
    - client_secret
    - client_access_token
    """
    with open('genius-api.json') as f:
        api_info = json.load(f)
    return api_info


def get_artist_songs(artist_name: str, api_info: dict) -> pd.DataFrame:
    """
    Returns a pandas DataFrame with the lyrics of the songs of the given artist.
    """
    genius = lg.Genius(api_info['client_access_token'], timeout=60)
    artist = genius.search_artist(artist_name)
    songs_df = pd.DataFrame(columns=['song_name', 'song_lyrics'])
    for song in artist.songs:
        songs_df = songs_df.append(
            {'song_name': song.title, 'song_lyrics': song.lyrics}, ignore_index=True)
    return songs_df


def write_lyrics_to_csv(artist_name: str, songs_df: pd.DataFrame) -> None:
    """
    Writes the lyrics of the songs of the given artist to a CSV file.
    """
    songs_df.to_csv(OUTPUT_FILE_PREFIX + artist_name + OUTPUT_FILE_SUFFIX)


def main(artist_name):
    api_info = read_api_info()
    songs_df = get_artist_songs(artist_name, api_info)
    write_lyrics_to_csv(artist_name, songs_df)


if __name__ == '__main__':
    artists_names = ['The Beatles', 'Pink Floyd',
                     'Queen', 'Led Zeppelin', 'Guns N’ Roses']
    for artist_name in artists_names:
        main(artist_name)
