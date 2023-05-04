import pygame
from pygame import mixer

class AudioManager:
    def __init__(self):
        self.songs = {}
        self.sound_effects = {}
        self.current_song = None

    def load_song(self, name, filepath):
        self.songs[name] = filepath

    def load_sound_effect(self, name, filepath):
        self.sound_effects[name] = mixer.Sound(filepath)

    def play_song(self, name, loops=-1, fade_time=0):
        if self.current_song:
            mixer.music.fadeout(fade_time)
        if name in self.songs:
            mixer.music.load(self.songs[name])
            mixer.music.play(loops)
            self.current_song = name

    def stop_song(self):
        if self.current_song:
            mixer.music.stop()
            self.current_song = None

    def play_sound_effect(self, name, loops=0):
        if name in self.sound_effects:
            sound = self.sound_effects[name]
            return sound.play(loops)


    def stop_sound_effect(self, name):
        if name in self.sound_effects:
            self.sound_effects[name].stop()

    def set_volume(self, volume):
        mixer.music.set_volume(volume)

    def fade_out_all(self, fade_time):
        if self.current_song:
            mixer.music.fadeout(fade_time)
            self.current_song = None

        for sound in self.sound_effects.values():
            channels = mixer.find_channel(True)
            for channel in channels:
                if channel.get_busy() and channel.get_sound() == sound:
                    channel.fadeout(fade_time)