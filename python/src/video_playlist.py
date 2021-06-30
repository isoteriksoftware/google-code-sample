"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self) -> None:
        self._videos = []

    @property
    def videos(self): 
        return self._videos

    def has_video(self, video):
        return video.title in self._videos
    
    def add_video(self, video):
        self._videos.append(video.title)
