import json
import os
from datetime import datetime
from pathlib import Path

FILEPATH = Path(__file__).parent.absolute() / "settings.json"

settings = None

def load_settings_file():
    if not os.path.exists(FILEPATH):
        exit(f'ERROR: Could not load settings from {FILEPATH}')
    
    file = open(FILEPATH)
    
    global settings
    settings = json.load(file)

    print(f'Successfully loaded settings from {FILEPATH}')

    file.close()

def get_setting(name: str):
    if settings == None:
        load_settings_file()
    
    if name not in settings:
        exit(f'ERROR: {name} is not a valid setting')
    
    return settings[name]

def get_setting_as_date(name: str, format: str, timezone):
    if settings == None:
        load_settings_file()

    if name not in settings:
        exit(f'ERROR: {name} is not a valid setting')
    
    try:
        return datetime.strptime(settings[name], format).replace(tzinfo=timezone)
    except ValueError:
        exit(f'ERROR: {name} is not a valid date')
