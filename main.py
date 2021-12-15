from Classes import *
import SteamAPI
import json

playerList = {}

player = 0

trouves = 1

api_key_ = "C7B6778C18122B43DAC03A1FF65F43AF"
valtyk_steam_id = "76561198153919062"

maxReached = False

atraiter = [valtyk_steam_id]
idActu = 0

while len(playerList) < 100 and len(atraiter) > 0:
    idActu = atraiter[0]
    atraiter = atraiter[1:]
    try:
        summary = SteamAPI.ISteamUser.GetPlayerSummaries(api_key_, idActu)
    except:
        continue
    player = Player(idActu, summary["response"]["players"][0]["personaname"])
    playerList[idActu] = player
    print("Population de la liste:", trouves, "/ 100")
    trouves += 1
    try:
        friendlist = SteamAPI.ISteamUser.GetFriendList(api_key_, idActu)
    except:
        continue
    if len(playerList.keys()) + len(atraiter) < 100:
        for i in friendlist["friendslist"]["friends"]:
            if (len(playerList.keys()) + len(atraiter)) >= 100:
                break
            elif i["steamid"] not in playerList.keys() and i["steamid"] not in atraiter:
                atraiter.append(i["steamid"])