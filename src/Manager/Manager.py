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

    pyautogui.PAUSE = 2.5
    SECS_BETWEEN_KEYS = 0.01

    def __init__(self):
        if not os.path.exists(os.path.relpath('config')):
            os.mkdir('config')

        self.data = self.load_json()
        self.sort_data()
        self.arguments = []
        self.language = self.get_current_language()

    def run(self, login, password):
        # clean up processes and start from scratch, its easier            
        self.shut_down_client()

        pid = self.run_league_client()
        debug(f'PID of league client: {pid}')

        self.type_username(login)
        self.type_password(password)
        self.confirm()
    
    def run_league_client(self):
        x = subprocess.Popen([LEAGUE_PATH, *self.arguments])

        return x.pid

    def type_username(self, login):
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

    def monitor_league_client(self):
        sleep(5) # need to wait for new league client process, idk why is it like that
        client_pid = -1
        found_client = False
        while not found_client:
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                if proc.info['name'] == 'LeagueClient.exe': 
                    client_pid = proc.info['pid']
                    debug(f'Found League client pid: {client_pid}')
                    found_client = True
                    break
            sleep(2)

        client_exists = True
        while client_exists:
            client_exists = False
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                if proc.info['name'] == 'LeagueClient.exe': 
                    client_pid = proc.info['pid']
                    debug(f'Client exists: {client_pid}')
                    client_exists = True
            sleep(2)
        debug(f'Client closed')
        sleep(1)

    def sign_out(self):
        sleep(1)
        location = pyautogui.center(pyautogui.locateOnScreen('assets\\close_client.png', grayscale=False))
        pyautogui.click(x=location.x, y=location.y, _pause=False)
        sleep(1)
        location = pyautogui.center(pyautogui.locateOnScreen('assets\\sign_out.png'))
        pyautogui.click(x=location.x, y=location.y, _pause=False)


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
