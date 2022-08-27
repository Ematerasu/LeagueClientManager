from time import sleep
import os
import json
import subprocess
import yaml

import psutil
import pyautogui
from pyautogui import ImageNotFoundException

from utils import LANGUAGES, debug
from config import DATA_PATH, LEAGUE_PATH, CONFIG_PATH

class Manager:
    """_summary_
        Main class for manager, contains all functions that run
        LeagueClient and log user in
    """
    pyautogui.PAUSE = 2.5
    SECS_BETWEEN_KEYS = 0.01

    def __init__(self):

        # if folder for json's doesn't exist -> create it
        if not os.path.exists(os.path.relpath('config')):
            os.mkdir('config')

        #load accounts, sort them (visual upgrade)
        self.data = self.load_json()
        self.sort_data()
        # language settings
        self.arguments = []
        self.language = self.get_current_language()

    def run(self, login, password):
        """_summary_
            run LeagueClient and log user in
        Args:
            login (string): user's login
            password (string): user's password
        """

        # clean up processes and start from scratch, its easier            
        self.shut_down_client()

        pid = self.run_league_client()
        debug(f'PID of league client: {pid}')

        self.type_username(login)
        self.type_password(password)
        self.confirm()
    
    def run_league_client(self):
        """_summary_
            Simply run league client
        Returns:
            int: pid of league client, for now we only use it for debug purposes
            because after login this process ends and starts new one (that's weird but es como es)
        """        
        x = subprocess.Popen([LEAGUE_PATH, *self.arguments])

        return x.pid

    def type_username(self, login):
        """_summary_
            Wait for league client to pop up on screen, we do this by waiting for
            main_menu jpg (check assets folder), we can't just check processes because it takes some time
            till we can type login
        Args:
            login (string): user's login
        """        

        # wait for client to pop up on screen
        menu_icon = None
        while menu_icon is None:
            try:
                menu_icon = pyautogui.locateOnScreen('assets\\main_menu.png', grayscale=False)
            except ImageNotFoundException:
                sleep(0.5)

        debug('Client open!')
        pyautogui.typewrite(login, interval=self.SECS_BETWEEN_KEYS, _pause=False)

    def type_password(self, password):
        pyautogui.press('tab', _pause=False)
        pyautogui.typewrite(password, interval=self.SECS_BETWEEN_KEYS, _pause=False)

    def confirm(self):
        sleep(0.1)
        pyautogui.press('tab', _pause=False, presses=5)
        pyautogui.press('enter', _pause=False)

    def shut_down_client(self):
        sleep(1)
        self_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['pid'] == self_pid:
                continue
            if 'league' in proc.info['name'].lower() or 'riotclient' in proc.info['name'].lower():
                debug(proc.info['name'])
                proc.terminate()
                debug(f'Shut down process {proc.info}')
        debug('shut down finished')

    @staticmethod
    def league_client_exists():
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            if proc.info['name'] == 'LeagueClient.exe': 
                return True
        return False

    def load_json(self):
        """_summary_
            load accounts from json, if json doesn't exists then create empty one
        Returns:
            _type_: _description_
        """        
        if os.path.isfile(DATA_PATH):
            data = {}
            with open(DATA_PATH, 'r') as f:
                data = json.loads(f.read())
            return data
        with open(DATA_PATH, 'w') as f:
            f.write('{}')
        return {}

    def save_account(self, nick, login, password):
        self.data[nick] = {
            "login": login,
            "password": password
        }
        with open(DATA_PATH, 'w') as f:
            f.write(json.dumps(self.data, indent=4, sort_keys=True))

    def delete_accounts(self, nicks):
        for nick in nicks:
            del self.data[nick]
        with open(DATA_PATH, 'w') as f:
            f.write(json.dumps(self.data, indent=4, sort_keys=True))

    def sort_data(self):
        self.data = dict(sorted(self.data.items()))

    def change_language(self, language):
        """_summary_
            Change yaml config file, you can check its structure (path in config.py) and add argument to use when running league client process
            which is -locale={language} flag
            In yaml file all we need to do is change two variables as coded below
        Args:
            language (string): name of language
        """        
        if language == self.language:
            debug('Language is the same as the current language')
            return

        self.arguments.append(f'–locale={LANGUAGES[language]}')

        with open(CONFIG_PATH, 'r') as f:
            configs = yaml.safe_load(f)
        
        configs['install']['globals']['locale'] = LANGUAGES[language]
        configs['install']['patcher']['locales'] = [LANGUAGES[language]]

        with open(CONFIG_PATH, 'w') as f:
            yaml.dump(configs, f)

        self.language = language

    def get_current_language(self):
        with open(CONFIG_PATH, 'r') as f:
            configs = yaml.safe_load(f)
            language = configs['install']['globals']['locale']

        for key, value in LANGUAGES.items():
            if value == language:
                return key
        return 'English'
