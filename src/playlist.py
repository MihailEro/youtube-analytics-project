import os

from googleapiclient.discovery import build

from datetime import timedelta

import isodate

class PlayList:
    api_key = os.getenv('API_KEY_YT')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):

        self.playlist_id = playlist_id
        playlist_response = PlayList.youtube.playlists().list(part='snippet', id=self.playlist_id).execute()
        playlist_videos = PlayList.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                           part='contentDetails',
                                                           maxResults=50,
                                                           ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_response = PlayList.youtube.videos().list(part='contentDetails,statistics',
                                                        id=','.join(video_ids)
                                                        ).execute()

        self.title = playlist_response["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):

        total_duration = timedelta()
        for video in self.video_response['items']:
                # YouTube video duration is in ISO 8601 format
                iso_8601_duration = video['contentDetails']['duration']
                duration = isodate.parse_duration(iso_8601_duration)
                total_duration += duration
        return total_duration

    def show_best_video(self):
        likes = 0
        max_likes_video_id = ""

        for video in self.video_response["items"]:
            if int(video["statistics"]["likeCount"]) > likes:
                    likes = int(video["statistics"]["likeCount"])
                    max_likes_video_id = video["id"]
        return f"https://youtu.be/{max_likes_video_id}"