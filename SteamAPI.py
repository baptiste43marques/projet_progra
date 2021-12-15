import urllib
import json

class ISteamNews:
    @staticmethod
    def GetNewsForApp(appid = 440, count = 3, maxlength = 300, formatS = "json"):
        version = "v0002"
        parameters = {}
        parameters["appid"] = appid
        parameters["count"] = count
        parameters["maxlength"] = maxlength
        parameters["format"] = formatS
        return globalRequest("ISteamNews", "GetNewsForApp", version, parameters)
        
class ISteamUserStats:
    @staticmethod
    def GetGlobalAchievementPercentagesForApp(gameid = 440, formatS = "json"):
        version = "v0002"
        parameters = {}
        parameters["gameid"] = gameid
        parameters["format"] = formatS
        return globalRequest("ISteamUserStats", "GetGlobalAchievementsPercentagesForApp", version, parameters)
    
    @staticmethod
    def GetPlayerAchievements(key, appid = 440, steamid = "76561197960435530"):
        version = "v0001"
        parameters = {}
        parameters["appid"] = appid
        parameters["key"] = key
        parameters["steamid"] = steamid
        return globalRequest("ISteamUserStats", "GetPlayerAchievements", version, parameters)
    
    @staticmethod
    def GetUserStatsForGame(key, appid = 440, steamid = "76561197960435530"):
        version = "v0002"
        parameters = {}
        parameters["appid"] = appid
        parameters["key"] = key
        parameters["steamid"] = steamid
        return globalRequest("ISteamUserStats", "GetUserStatsForGame", version, parameters)
    
class ISteamUser:
    @staticmethod
    def GetPlayerSummaries(key, steamids = "76561197960435530", formatS = "json"):
        version = "v0002"
        parameters = {}
        parameters["key"] = key
        parameters["steamids"] = steamids
        parameters["format"] = formatS
        return globalRequest("ISteamUser", "GetPlayerSummaries", version, parameters)
    
    @staticmethod
    def GetFriendList(key, steamid = "76561197960435530", relationship = "friend", formatS = "json"):
        version = "v0001"
        parameters = {}
        parameters["key"] = key
        parameters["steamid"] = steamid
        parameters["relationship"] = relationship
        parameters["format"] = formatS
        return globalRequest("ISteamUser", "GetFriendList", version, parameters)

class IPlayerService:
    @staticmethod
    def GetOwnedGames(key, steamid = "76561197960434622", include_appinfo = False, include_played_free_games = False, formatS = "json"):
        version = "v0001"
        parameters = {}
        parameters["key"] = key
        parameters["steamid"] = steamid
        parameters["format"] = formatS
        if include_appinfo:
            parameters["include_appinfo"] = "true"
        if include_played_free_games:
            parameters["include_played_free_games"] = "true"
        return globalRequest("IPlayerService", "GetOwnedGames", version, parameters)
    
    @staticmethod
    def GetRecentlyPlayedGames(key, steamid = "76561197960434622", count = "100", formatS = "json"):
        version = "v0001"
        parameters = {}
        parameters["key"] = key
        parameters["steamid"] = steamid
        parameters["count"] = count
        parameters["format"] = formatS
        return globalRequest("IPlayerService", "GetRecentlyPlayedGames", version, parameters)

def globalRequest(module, function, version, parameters):
    url = "http://api.steampowered.com/" + module + "/" + function + "/" + version + "/?"
    for i in parameters.keys():
        url += i + "=" + parameters[i]
        if i != list(parameters.keys())[len(list(parameters.keys())) - 1]:
            url += "&"
    response =  urllib.request.urlopen(url)
    chaine = response.read().decode('utf-8')
    dictionnaire = json.loads(chaine)
    return dictionnaire