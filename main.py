from Classes import *
import SteamAPI
import json

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
while len(playerList) < 100 and len(atraiter) > 0:
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
    
    # TODO Ajouter au joueur la liste des jeux qu'il possède (avec les temps de jeux)
    
    # On ajoute le joueur au dictionnaire (avec son steamid comme clé)
    playerList[idActu] = player
    # Affichage qui indique la progression
    print("Population de la liste:", trouves, "/ 100")
    trouves += 1
    try:
        # On essaye de récupérer la liste d'amis du joueur
        friendlist = SteamAPI.ISteamUser.GetFriendList(api_key_, idActu)
    except:
        # Si une erreur survient, on skip sa liste d'amis
        continue
    # Si on a pas un total de 100 joueurs
    if len(playerList.keys()) + len(atraiter) < 100:
        # Alors on parcourt la liste des amis du joueur
        for i in friendlist["friendslist"]["friends"]:
            # Si on a déjà 100 personnes, on sort
            if (len(playerList.keys()) + len(atraiter)) >= 100:
                break
            # Sinon si l'id n'est pas déjà présent
            elif i["steamid"] not in playerList.keys() and i["steamid"] not in atraiter:
                # Alors on l'ajoute
                atraiter.append(i["steamid"])