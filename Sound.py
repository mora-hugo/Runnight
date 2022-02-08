import pygame
import json

class Sound():
    
    def __init__(self):
        
        
        f = open('Data/config/config.json', 'r')
        self.data = json.load(f)
        f.close()
        pygame.mixer.set_num_channels(2)
        self.sound = {}
        for i in self.data["Sounds"]:
            self.sound[i] = pygame.mixer.Sound(self.data["Sounds"][i])
        



    def playSound(self,name,volume):

        canal_1 = pygame.mixer.Channel(0)
        canal_1.set_volume(volume)
        canal_1.play(self.sound[name])
        
