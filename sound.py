import pygame as pg 
import time


class Sound:
    def __init__(self): 
        self.music_normal = "sounds/ride_of_the_valkyries.mp3"
        self.music_fast = "sounds/ride_of_the_valkyries3.wav"
        self.music_faster = "sounds/ride_of_the_valkyries5.wav"

        self.pickup = pg.mixer.Sound('sounds/pickup.wav')
        self.gameover = pg.mixer.Sound('sounds/gameover.wav')
        self.thugles = pg.mixer.Sound('sounds/Thugles.wav')

        pg.mixer.music.load(self.music_normal)
        pg.mixer.music.set_volume(0.2)
                                             
    def play_background(self): 
        pg.mixer.music.play(-1, 0.0)
        self.music_playing = True

    def reset_track(self):
        pg.mixer.music.load(self.music_normal)
        self.play_background()

    def change_music_speed(self, track_number):
        """Change background music based on the number of aliens left."""
        if track_number == 1:
            pg.mixer.music.load(self.music_fast)
            self.play_background()
        elif  track_number == 2:
            pg.mixer.music.load(self.music_faster)
            self.play_background()
        
    def play_pickup(self): 
        if self.music_playing: self.pickup.play()
        
    def play_gameover(self):
        if self.music_playing: 
            self.stop_background()
            self.gameover.play()
            time.sleep(3.0)       # sleep until game over sound has finished

    def play_thugles(self):
        self.stop_background()
        self.thugles.play()
                    
    def toggle_background(self):
        if self.music_playing: 
            self.stop_background()
        else:
            self.play_background()
        self.music_playing = not self.music_playing
        
    def stop_background(self): 
        pg.mixer.music.stop()
        self.music_playing = False 