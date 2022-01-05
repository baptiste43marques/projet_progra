from Classes import *
import SteamAPI
import json
from matplotlib import pyplot

limiteEchantillon = 500
limiteJeuxGraphiques = 100

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
    except:
        # Si on ne peut pas à cause d'une erreur, on skip le joueur
        continue
    # On récupère son pseudo
    player = Player(idActu, summary["response"]["players"][0]["personaname"])
    
    # On récupère sa liste de jeux possédés et récemment joués
    allGames = SteamAPI.IPlayerService.GetOwnedGames(api_key_, idActu, include_appinfo = True, include_played_free_games = True)
    recentGames = SteamAPI.IPlayerService.GetRecentlyPlayedGames(api_key_, idActu)
    
    # On essaye d'obtenir les informations sur les jeux et de les instancier.
    # Si ça échoue, on passe à la personne suivante
    try:
        for i in allGames["response"]["games"]:
            jeu = Game(i["appid"], i["name"], i["playtime_forever"])
            player.addOwnedGame(jeu)
    
        # Idem pour les jeux récents   
        for i in recentGames["response"]["games"]:
            jeu = Game(i["appid"], i["name"], i["playtime_2weeks"])
            player.addRecentGame(jeu)
    except:
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

# Un tableau récapitulatif
donnees = []

# On insère, pour chaque jeu, les données sous la forme: [nom de jeu, utilisateurs, joueurs récents]
for i in jeuxOrdre.keys():
    if i in recentOrdre.keys():
        fin = recentOrdre[i]
    else:
        fin = 0
    donnees.append([i, jeuxOrdre[i], fin])

# La colonne 1 du tableau, qui équivaut au nombre de personne possédant un jeu
possessions = [i[1] for i in donnees][0:limiteJeuxGraphiques]
# La colonne 2, qui équivaut au nombre de joueurs récents
joues = [i[2] for i in donnees][0:limiteJeuxGraphiques]
pyplot.bar(range(limiteJeuxGraphiques), possessions)
pyplot.bar(range(limiteJeuxGraphiques), joues)