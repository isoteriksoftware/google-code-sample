"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, original_name, formatted_name) -> None:
        self._videos = []
        self._original_name = original_name
        self._formatted_name = formatted_name

    @property
    def videos(self): 
        return self._videos
    
    @property
    def original_name(self): 
        return self._original_name

    @property
    def formatted_name(self): 
        return self._formatted_name

    def has_video(self, video):
        return video.video_id in self._videos
    
    def add_video(self, video):
        self._videos.append(video.video_id)

    def remove_video(self, video):
        self._videos.remove(video.video_id)

    def clear(self):
        self._videos.clear()