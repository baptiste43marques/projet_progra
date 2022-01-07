from Classes import *
import SteamAPI
import json
from matplotlib import pyplot

limiteEchantillon = 100
limiteGraphique = 100
limiteNbJeux = 250

# Notre échantillon de données
playerList = {}

# Initialisation d'une instance de joueur
player = 0

# On a au début un seul ID Steam
trouves = 1

# La clé qui permet l'accèsà l'API
api_key_ = "C7B6778C18122B43DAC03A1FF65F43AF"
# Mon steamId qui servira de base
valtyk_steam_id = "76561198153919062"

# Le seul id à traiter au début est le mien
atraiter = [valtyk_steam_id]
# L'id en cours de traitement
idActu = 0

# Tant qu'on a pas 100 personnes et qu'on trouve encore des gens:
while len(playerList) < limiteEchantillon and len(atraiter) > 0:
    # On extrait le premier id de la liste
    idActu = atraiter[0]
    atraiter = atraiter[1:]
    try:
        # Et on essaye de recupérer ses informations
        summary = SteamAPI.ISteamUser.GetPlayerSummaries(api_key_, idActu)
        # On récupère son pseudo
        player = Player(idActu, summary["response"]["players"][0]["personaname"])
        
        # On récupère sa liste de jeux possédés et récemment joués
        allGames = SteamAPI.IPlayerService.GetOwnedGames(api_key_, idActu, include_appinfo = True, include_played_free_games = True)
        recentGames = SteamAPI.IPlayerService.GetRecentlyPlayedGames(api_key_, idActu)
        
        # On essaye d'obtenir les informations sur les jeux et de les instancier.
        for i in allGames["response"]["games"]:
            jeu = Game(i["appid"], i["name"], i["playtime_forever"])
            player.addOwnedGame(jeu)
    
        # Idem pour les jeux récents   
        for i in recentGames["response"]["games"]:
            jeu = Game(i["appid"], i["name"], i["playtime_2weeks"])
            player.addRecentGame(jeu)
    except:
        # Si ça échoue, on passe à la personne suivante
        continue
    
    # On ajoute le joueur au dictionnaire (avec son steamid comme clé)
    playerList[idActu] = player
    # Affichage qui indique la progression
    print("Population de la liste:", trouves, "/", limiteEchantillon)
    trouves += 1
    try:
        # On essaye de récupérer la liste d'amis du joueur
        friendlist = SteamAPI.ISteamUser.GetFriendList(api_key_, idActu)
    except:
        # Si une erreur survient, on skip sa liste d'amis
        continue
    # Si on n'a pas atteint la limite de joueurs
    if len(playerList.keys()) + len(atraiter) < limiteEchantillon:
        # Alors on parcourt la liste des amis du joueur
        for i in friendlist["friendslist"]["friends"]:
            # Si on a déjà atteint la limite, on sort
            if (len(playerList.keys()) + len(atraiter)) >= limiteEchantillon:
                break
            # Sinon si l'id n'est pas déjà présent
            elif i["steamid"] not in playerList.keys() and i["steamid"] not in atraiter:
                # Alors on l'ajoute
                atraiter.append(i["steamid"])

# Le compte pour chaque jeu
compteJeux = {}
# Le compte des joueurs récents
compteRecents = {}

# On ajoute aux dicos, pour chaque nom de jeu, le nombre de personnes possédant le jeu
# ainsi que le nombre de personnes y ayant joué récemment
for i in playerList.keys():
    for j in playerList[i].allGameList.keys():
        if playerList[i].allGameList[j].name not in compteJeux.keys():
            compteJeux[playerList[i].allGameList[j].name] = 1
        else:
            compteJeux[playerList[i].allGameList[j].name] = compteJeux[playerList[i].allGameList[j].name] + 1
            
    for j in playerList[i].recentGameList.keys():
        if playerList[i].recentGameList[j].name not in compteRecents.keys():
            compteRecents[playerList[i].recentGameList[j].name] = 1
        else:
            compteRecents[playerList[i].recentGameList[j].name] = compteRecents[playerList[i].recentGameList[j].name] + 1

# On ordonne les jeux par nombre de joeuurs décroissants
jeuxOrdre = dict(sorted(compteJeux.items(), key = lambda x:x[1], reverse = True))
recentOrdre = dict(sorted(compteRecents.items(), key = lambda x:x[1], reverse = True))

# Un tableau récapitulatif par jeu
donnees = []

# On insère, pour chaque jeu, les données sous la forme: [nom de jeu, utilisateurs, joueurs récents]
for i in jeuxOrdre.keys():
    if i in recentOrdre.keys():
        fin = recentOrdre[i]
    else:
        fin = 0
    donnees.append([i, jeuxOrdre[i], fin])

# La colonne 1 du tableau, qui équivaut au nombre de personne possédant un jeu
possessions = [i[1] for i in donnees][0:limiteGraphique]
# La colonne 2, qui équivaut au nombre de joueurs récents
joues = [i[2] for i in donnees][0:limiteGraphique]

# Création du premier graphique
titre = ""
pyplot.bar(range(len(possessions)), possessions)
pyplot.bar(range(len(joues)), joues)
pyplot.ylabel("Bleu: nombre de personnes ayant le jeu\nOrange: personnes ayant joué récemment au jeu")
pyplot.xlabel("Numéros de jeu, classés par possession totale")
titre = titre + list(jeuxOrdre.keys())[0] + ", " + list(jeuxOrdre.keys())[1] + ", " + list(jeuxOrdre.keys())[2]
pyplot.title(titre)

pyplot.show()
pyplot.clf()

# Le 2e tableau, par joueur cette fois
donnees2 = []

# Pour chaque joueur, on insère son ID, le nombre de jeux possédés et le nombre de jeux auquel il a joué
for i in playerList.keys():
    if(len(playerList[i].allGameList) <= limiteNbJeux):
        donnees2.append([i, len(playerList[i].allGameList), len(playerList[i].recentGameList)])

# La colonne 1, le nombre de jeux possédés
possessions2 = [i[1] for i in donnees2][0:limiteGraphique]
# La colonne 2, le nombre de jeux lancés récemment
joues2 = [i[2] for i in donnees2][0:limiteGraphique]
# Création du 2e graphique
pyplot.bar(range(len(possessions2)), possessions2)
pyplot.bar(range(len(joues2)), joues2)
pyplot.ylabel("Bleu: nombre de jeux possédés\nOrange: nombre de jeux ayant été lancés récemment")
pyplot.xlabel("Numéro de personne")

pyplot.show()
pyplot.clf()

# 3e set de données, identique au premier mais ordonné différemment
donnees3 = []

# On insère, pour chaque jeu, les données sous la forme: [nom de jeu, utilisateurs, joueurs récents]
for i in recentOrdre.keys():
    if i in jeuxOrdre.keys():
        mid = jeuxOrdre[i]
    else:
        mid = 0
    donnees3.append([i, mid, recentOrdre[i]])

# La colonne 1 du tableau, qui équivaut au nombre de personne possédant un jeu
possessions3 = [i[1] for i in donnees3][0:limiteGraphique]
# La colonne 2, qui équivaut au nombre de joueurs récents
joues3 = [i[2] for i in donnees3][0:limiteGraphique]

# Création du troisième graphique
titre = ""
pyplot.bar(range(len(possessions)), possessions3)
pyplot.bar(range(len(joues)), joues3)
pyplot.ylabel("Bleu: nombre de personnes ayant le jeu\nOrange: personnes ayant joué récemment au jeu")
pyplot.xlabel("Numéros de jeu, classés par popularité actuelle")
titre = titre + list(recentOrdre.keys())[0] + ", " + list(recentOrdre.keys())[1] + ", " + list(recentOrdre.keys())[2]
pyplot.title(titre)

pyplot.show()