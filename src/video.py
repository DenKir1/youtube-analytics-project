from src.channel import Channel


class Video(Channel):

    def __init__(self, video_id):
        youtube = super().get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.video_response = video_response
        self.__video_id = video_id
        self.title = video_response['items'][0]['snippet']['title']
        self.description = video_response['items'][0]['snippet']['description']
        self.url = f'https://youtu.be/{self.video_id}'
        self.like = video_response['items'][0]['statistics']['likeCount']
        self.view = video_response['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f"{self.title}"

    @property
    def video_id(self):
        return self.__video_id


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        youtube = super().get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails, snippet',
                                                       maxResults=50,
                                                       ).execute()
        self.playlist_id = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
