class InventoryItem():
    def __init__(self,name,stats,type,player):
        self.name = name
        self.stats = stats
        self.player = player
        self.type = type
        
    def kill(self):
        self.player.inventory["Plats"][self.name].remove(self)