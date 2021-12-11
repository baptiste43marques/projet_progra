from Classes import *
import xmltodict
import SteamAPI
import json

playerList = []

api_key_ = "C7B6778C18122B43DAC03A1FF65F43AF"
valtyk_steam_id = "76561198153919062"

test_data = SteamAPI.IPlayerService.GetRecentlyPlayedGames(api_key_, steamid = valtyk_steam_id)
data_string = test_data.read().decode('utf-8')
dictionnaire = json.loads(data_string)
