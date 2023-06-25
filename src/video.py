import os

from googleapiclient.discovery import build


class Video:
    api_key = os.getenv('API_KEY_YT')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=video_id
                                                     ).execute()
        try:
            self.video_title = video_response['items'][0]['snippet']['title']
            self.video_url = 'https://www.youtube.com/watch?v=' + self.__video_id
            self.view_count = int(video_response['items'][0]['statistics']['viewCount'])
            self.like_count = int(video_response['items'][0]['statistics']['likeCount'])
        except:
            self.title = None
            self.video_url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.video_title

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id