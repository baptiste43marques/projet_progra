# Classe abstraite, ne pas instancier sans enfant
class SteamObject:
    identifier = -1
    name = ""
    
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name

# Stocke un objet de type "joueur" avec sa liste de jeu
class Player(SteamObject):
    gameList = []
    
    def __init__(self, identifier, name):
        super.init(identifier, name)
        
    def addGame(self, game):
        self.gameList.append(game)
        
# Stocke un objet de type "jeu" avec le temps passé dessus.
# Plusieurs instances du même jeu peuvent exister
class Game(SteamObject):
    playtime_2weeks = -1
    playtime_forever = -1
    
    def __init__(self, identifier, name, play2week, playforever):
        super.init(identifier, name)
        self.playtime_2weeks = play2week
        self.playtime_forever = playforever
        
    @staticmethod
    def sortGameByRecentPlay(game1, game2):
        return game1.playtime_2weeks < game2.playtime_2weeks
    
    @staticmethod
    def sortGameByTotalPlay(game1, game2):
        return game1.playtime_forever < game2.playtime_forever
        
    