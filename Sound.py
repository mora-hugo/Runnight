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
        self.canal_2 = pygame.mixer.Channel(1)

        self.soundM =  pygame.mixer.Sound(self.data["Sounds"]["groar"])
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
        if (biome == "foret" or biome == "ville"):
            if(night == "day"):
                pygame.mixer.music.load( self.music['dayMusic'] )
            else:
                pygame.mixer.music.load( self.music['nightMusic'] )
        elif (biome == "house"):
                pygame.mixer.music.load( self.music['house'] )
        elif (biome == "menu"):
                pygame.mixer.music.load( self.music['menu'] )
        
        pygame.mixer.music.play(-1,0,0)

    def MonsterGroar(self,volume):
        self.canal_2.set_volume(volume)
        self.canal_2.play(self.soundM)

    def StopGroar(self):
        self.canal_2.stop()