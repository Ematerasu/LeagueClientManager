import os
import re
import win32api

from config import DEBUG

def debug(msg):
    if DEBUG:
        print(msg)

LANGUAGES = {
    'English': 'eu_GB',
    'French': 'fr_FR',
    'Polish': 'pl_PL',
    'Japanese': 'ja_JP',
    'Korean': 'ko_KR',
    'Chinese': 'zh_CN',
    'Taiwanese': 'zh_TW',
    'Spanish (Spain)': 'es_ES',
    'Spanish (Latin America)': 'es_MX',
    'German': 'de_DE',
    'Italian': 'it_IT',
    'Romanian': 'ro_RO',
    'Greek': 'el_GR',
    'Portuguese': 'pt_BR',
    'Hungarian': 'hu_HU',
    'Russian': 'ru_RU',
    'Turkish': 'tr_TR',
}

def find(root_folder, rex):
    for root,dirs,files in os.walk(root_folder):
        for f in files:
            result = rex.search(f)
            if result:
                return os.path.join(root, f)
    return False

def find_in_all_drives(file_name):
    #create a regular expression for the file
    rex = re.compile(file_name)
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        x = find( drive, rex )
        if x:
            return x
    return None

def remove_garbage(path):
    to_return = []
    for elem in path:
        if elem == 'Riot Games':
            to_return.append(elem)
            return to_return
        to_return.append(elem)