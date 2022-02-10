class InventoryItem():
    def __init__(self,name,stats,type,player):
        self.name = name
        self.stats = stats/100
        self.player = player
        self.type = type
        
    def kill(self):
        self.player.inventory["Plats"][self.name].remove(self)