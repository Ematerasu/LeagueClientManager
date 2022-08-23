import os

DEBUG = True
RIOT_GAMES_PATH = 'C:\\Riot Games\\'
LEAGUE_PATH = RIOT_GAMES_PATH + 'League of Legends\\LeagueClient.exe' # default path for LeagueClient.exe
DATA_PATH = os.path.relpath('config\\data.json')
CONFIG_PATH = RIOT_GAMES_PATH + 'League of Legends\Config\\LeagueClientSettings.yaml'
