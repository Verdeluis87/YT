import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
API_KEY=os.getenv("API_KEY")

def get_playlist_id(channel_handle):

    try:

        url=f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}"

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        channel_playlistId=data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        return channel_playlistId

    except requests.exceptions.RequestException as e:
        raise e

if __name__=="__main__":
    playlist_id=get_playlist_id("MrBeast")
    print(playlist_id)
else:
    pass