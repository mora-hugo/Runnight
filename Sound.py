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
        self.canal_1 = pygame.mixer.Channel(0)

        self.music = {}
        for i in self.data["Music"]:
            self.music[i] = self.data["Music"][i]
           


    def playSound(self,name,volume):
        self.canal_1.set_volume(volume)
        self.canal_1.play(self.sound[name])
        
    def StopSound(self):
        self.canal_1.stop()

    def playMusic(self,biome,night,volume):
        pygame.mixer.music.stop()
        pygame.mixer.music.set_volume(volume)
        if (biome == "forest"):
            if(not night):
                pygame.mixer.music.load( self.music['dayMusic'] )
            else:
                pygame.mixer.music.load( self.music['nightMusic'] )
        elif (biome == "house"):
                pygame.mixer.music.load( self.music['house'] )
        elif (biome == "menu"):
                pygame.mixer.music.load( self.music['menu'] )
        else:
            if(not night):
                pygame.mixer.music.load( self.music['dayMusic'] )
            else:
                pygame.mixer.music.load( self.music['nightMusic'] )
        
        pygame.mixer.music.play(-1,0,0)