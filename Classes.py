# Classe abstraite, ne pas instancier seule
class SteamObject:
    identifier = -1
    name = ""
    
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name

# Stocke un objet de type "joueur" avec sa liste de jeu possédé et sa liste de jeux récents
class Player(SteamObject):
    recentGameList = 0
    allGameList = 0
    
    def __init__(self, identifier, name):
        super().__init__(identifier, name)
        self.recentGameList = {}
        self.allGameList = {}
        
    def addRecentGame(self, game):
        self.recentGameList[game.identifier] = game
        
    def addOwnedGame(self, game):
        self.allGameList[game.identifier] = game
        
# Stocke un objet de type "jeu" avec le temps passé dessus.
# Plusieurs instances du même jeu peuvent exister
class Game(SteamObject):
    playtime = 0
    
    def __init__(self, identifier, name, play):
        super().__init__(identifier, name)
        self.playtime = play
    
    # Cette méthode permet de trier les jeux par temps de jeu.
    # ATTENTION ! Il faut bien distinguer les jeux ayant un temps de jeu récent et un temps de jeu total !
    @staticmethod
    def sortGameByPlayTime(game1, game2):
        return game1.playtime < game2.playtime
        
    