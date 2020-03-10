import pygame

class SongPlayer:
    def __init__(self): 
        self.current_song = None 
        
        pygame.mixer.init(48000)

    def PlaySong(self, song_file):
        pygame.mixer.music.load(song_file)
        pygame.mixer.music.play()

    def SetVolume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def UnPause(self):
        pygame.mixer.music.unpause()

    def Pause(self):
        pygame.mixer.music.pause()

    def Destroy(self):
        pygame.mixer.quit()
