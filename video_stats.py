import requests
import os
from dotenv import load_dotenv
from datetime import date
import json

load_dotenv(dotenv_path='.env')
API_KEY=os.getenv("API_KEY")
maxResults=50

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

def get_videos_id(playlistid):

    videosIds=[]

    pageToken=None

    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistid}&key={API_KEY}'

    try:
        while True:

            url=base_url

            if pageToken:
                url+=f'&pageToken={pageToken}'

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                videoId = item['contentDetails']['videoId']
                videosIds.append(videoId)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break

        return videosIds

    except requests.exceptions.RequestException as e:
        raise e



def extract_videos_data(video_ids):

    videos_data = []

    def batch_list(video_id_list, batch_size):
        for video_id in range(0, len(video_id_list), batch_size):
            yield video_id_list[video_id:video_id + batch_size]



    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ','.join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                content_details = item['contentDetails']
                statistics = item['statistics']

                video_data={
                    "video_id": video_id,
                    "title": snippet['title'],
                    "published_at": snippet['publishedAt'],
                    "duration": content_details['duration'],
                    "viewCount": statistics.get('viewCount', None),
                    "likeCount": statistics.get('likeCount', None),
                    "commentCount": statistics.get('commentCount', None)
                }

                videos_data.append(video_data)

        return videos_data

    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(videos_data):
    file_path = f'./data/YT_data_{date.today()}.json'

    with open(file_path, 'w', encoding='utf-8') as json_outfile:
        json.dump(videos_data, json_outfile, ensure_ascii=False, indent=4)



if __name__=="__main__":
    playlist_id=get_playlist_id("MrBeast")
    videos_ids=get_videos_id(playlist_id)
    video_data=extract_videos_data(videos_ids)
    save_to_json(video_data)
else:
    pass
