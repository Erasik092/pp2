import pygame
import os

class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        # Список файлов
        self.playlist = ["track_1.mp3", "track_2.mp3"] 
        self.current_idx = 0

    def play(self):
        if self.playlist:
            path = os.path.join(self.music_dir, self.playlist[self.current_idx])
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next_track(self):
        if self.playlist:
            self.current_idx = (self.current_idx + 1) % len(self.playlist)
            self.play()

    def prev_track(self):
        if self.playlist:
            self.current_idx = (self.current_idx - 1) % len(self.playlist)
            self.play()

    def get_current_name(self):
        if self.playlist:
            return self.playlist[self.current_idx]
        return "No Music Found"