"""A video player class."""

from src import video
from .video_library import VideoLibrary
from .video_playlist import Playlist
from random import choice

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_playing_video = None
        self._playlists = {}

    # Utility functions
    def sort_videos_by_title(self, video):
        return video.title

    def normalize_playlist_name(self, playlist_name):
        return playlist_name.replace(" ", "").lower()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        # Get the videos
        videos = self._video_library.get_all_videos()

        # Sort by title
        videos.sort(key = self.sort_videos_by_title)

        print("Here's a list of all available videos:")

        for video in videos:
            suffix = f" - FLAGGED (reason: {video.flag_reason})" if video.is_flagged else ""
            print(f"\t {video.title} ({video.video_id}) [{' '.join(video.tags)}]{suffix}")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        
        # Get the video
        video = self._video_library.get_video(video_id)

        # Make sure video exists
        if video:
            if video.is_flagged:
                print(f"Cannot play video: Video is currently flagged (reason: {video.flag_reason})")
                return

            # Stop any playing video
            if (self._current_playing_video):
                print(f"Stopping video: {self._current_playing_video.title}")
                self._current_playing_video.stop()
            
            # Play the current video
            self._current_playing_video = video
            print(f"Playing video: {self._current_playing_video.title}")
            self._current_playing_video.play()
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""

        # Stop the current playing video
        if (self._current_playing_video):
            print(f"Stopping video: {self._current_playing_video.title}")
            self._current_playing_video.stop()
            self._current_playing_video = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""

        # Get the videos
        videos = self._video_library.get_all_videos()
        if len(videos) == 0:
            print("No videos available")
            return

        # Make sure all videos are not flagged
        all_flaged = True
        for video in videos:
            if not video.is_flagged:
                all_flaged = False
                break

        if all_flaged:
            print("No videos available")
            return

        # Get a random video to play
        random_video = choice(videos)
        while random_video.is_flagged:
            random_video = choice(videos)

        # Play the video
        self.play_video(random_video.video_id)

    def pause_video(self):
        """Pauses the current video."""

        # Pause the current playing video
        if (self._current_playing_video):
            if (self._current_playing_video.is_paused):
                print(f"Video already paused: {self._current_playing_video.title}")
            else:
                self._current_playing_video.pause()
                print(f"Pausing video: {self._current_playing_video.title}")
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""

        # Continue the current playing video
        if (self._current_playing_video):
            if (not self._current_playing_video.is_paused):
                print("Cannot continue video: Video is not paused")
            else:
                self._current_playing_video.resume()
                print(f"Continuing video: {self._current_playing_video.title}")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""

        # Display the current playing video
        if (self._current_playing_video):
            paused_state = " - PAUSED" if self._current_playing_video.is_paused else ""
            video = self._current_playing_video
            print(f"Currently playing: {video.title} ({video.video_id}) [{' '.join(video.tags)}]{paused_state}")
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        name = self.normalize_playlist_name(playlist_name)
        if name in self._playlists:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlists[name] = Playlist(playlist_name, name)
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        
        name = self.normalize_playlist_name(playlist_name)
        if (name not in self._playlists):
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
            return
        
        playlist = self._playlists[name]
        video = self._video_library.get_video(video_id)
        if (not video):
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return

        if video.is_flagged:
            print(f"CCannot add video to my_playlist: Video is currently flagged (reason: {video.flag_reason})")
            return

        if (playlist.has_video(video)):
            print(f"Cannot add video to {playlist_name}: Video already added")
            return

        playlist.add_video(video)
        print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlists) == 0:
            print("No playlists exist yet")
            return

        print("Showing all playlists:")
        for name in sorted(self._playlists.keys()):
            playlist = self._playlists[name]
            print(f"\t{playlist.original_name}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        name = self.normalize_playlist_name(playlist_name)
        if (name not in self._playlists):
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return

        print(f"Showing playlist: {playlist_name}")

        playlist = self._playlists[name]
        if len(playlist.videos) == 0:
            print("No videos here yet")
        else:
            for video_id in playlist.videos:
                video = self._video_library.get_video(video_id)
                suffix = f" - FLAGGED (reason: {video.flag_reason})" if video.is_flagged else ""
                print(f"\t {video.title} ({video.video_id}) [{' '.join(video.tags)}]{suffix}")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        
        name = self.normalize_playlist_name(playlist_name)
        if (name not in self._playlists):
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return
        
        playlist = self._playlists[name]
        video = self._video_library.get_video(video_id)
        if (not video):
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return

        if (not playlist.has_video(video)):
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return

        playlist.remove_video(video)
        print(f"Removed video from {playlist_name}: {video.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        name = self.normalize_playlist_name(playlist_name)
        if (name not in self._playlists):
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
            return

        playlist = self._playlists[name]
        playlist.clear()
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        name = self.normalize_playlist_name(playlist_name)
        if (name not in self._playlists):
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
            return

        self._playlists.pop(name)
        print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        
        videos = []
        for video in self._video_library.get_all_videos():
            if not video.is_flagged and search_term.lower() in video.title.lower():
                videos.append(video)

        if len(videos) == 0:
            print(f"No search results for {search_term}")
            return

        videos.sort(key=self.sort_videos_by_title)

        print(f"Here are the results for {search_term}:")

        index = 1
        for video in videos:
            print(f"\t{index}) {video.title} ({video.video_id}) [{' '.join(video.tags)}]")
            index += 1

        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")

        chosen = input()

        if str.isnumeric(chosen):
            chosen_index = int(chosen) - 1
            if chosen_index >= 0 and chosen_index < len(videos):
                self.play_video(videos[chosen_index].video_id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        
        videos = []
        for video in self._video_library.get_all_videos():
            if not video.is_flagged:
                for tag in video.tags:
                    if video_tag.lower() == tag.lower():
                        videos.append(video)
                        break

        if len(videos) == 0:
            print(f"No search results for {video_tag}")
            return

        videos.sort(key=self.sort_videos_by_title)

        print(f"Here are the results for {video_tag}:")

        index = 1
        for video in videos:
            print(f"\t{index}) {video.title} ({video.video_id}) [{' '.join(video.tags)}]")
            index += 1

        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        
        chosen = input()

        if str.isnumeric(chosen):
            chosen_index = int(chosen) - 1
            if chosen_index >= 0 and chosen_index < len(videos):
                self.play_video(videos[chosen_index].video_id)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        
        video = self._video_library.get_video(video_id)
        if not video:
            print("Cannot flag video: Video does not exist")
            return

        if video.is_flagged:
            print("Cannot flag video: Video is already flagged")
            return

        reason = "Not supplied" if flag_reason == "" else flag_reason
        video.flag(reason)

        if video.is_playing or video.is_paused:
            self.stop_video()

        print(f"Successfully flagged video: {video.title} (reason: {reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        
        video = self._video_library.get_video(video_id)
        if not video:
            print("Cannot remove flag from video: Video does not exist")
            return

        if not video.is_flagged:
            print("Cannot remove flag from video: Video is not flagged")
            return

        print(f"Successfully removed flag from video: {video.title}")
