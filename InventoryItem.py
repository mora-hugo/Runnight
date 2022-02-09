class InventoryItem():
    def __init__(self,name,stats,player):
        self.name = name
        self.stats = stats
        self.player = player
        
    def kill(self):
        self.player.inventory["Plats"][self.name].remove(self)