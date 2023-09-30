from src.channel import Channel
from datetime import timedelta
import isodate


class MixinPlayList(Channel):

    def __init__(self, playlist_id):

        self.youtube = super().get_service()
        self.playlist_videos = self.get_playlist_videos(playlist_id)  # найдем имя плейлиста
        self.channel = self.playlist_videos['items'][0]['snippet']['channelId']  # из ID канала
        playlists = self.get_playlist()
        for playlist in playlists['items']:
            if playlist['id'] == playlist_id:  # и все потому, что нет названия в playlistItems
                self.title = playlist['snippet']['title']  # смотрю на это, как на костыль

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        self.video_response = video_response

    def get_playlist(self):
        playlists = self.youtube.playlists().list(channelId=self.channel,
                                                  part='contentDetails,snippet',
                                                  maxResults=50,
                                                  ).execute()
        return playlists

    def get_playlist_videos(self, playlist_id):
        playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails, snippet',
                                                            maxResults=50,
                                                            ).execute()

        return playlist_videos


class PlayList(MixinPlayList, Channel):

    def __init__(self, playlist_id):
        super().__init__(playlist_id)
        self.__playlist_id = playlist_id
        self.title = self.title
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def __str__(self):
        return f"{self.title}"

    @property
    def playlist_id(self):
        return self.__playlist_id

    @property
    def total_duration(self):
        duration_all = timedelta(0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_all += duration
        return duration_all

    def show_best_video(self):
        max_like = self.video_response['items'][0]
        for video in self.video_response['items']:
            if video['statistics']['likeCount'] > max_like['statistics']['likeCount']:
                max_like = video
        return f"https://youtu.be/{max_like['id']}"
