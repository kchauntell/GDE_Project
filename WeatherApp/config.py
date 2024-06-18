import os
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def get_config():
    if os.getenv('ENVIRONMENT') == 'production':
        return config['prod']
    elif os.getenv('ENVIRONMENT') == 'testing':
        return config['testing']
    else:
        return config['dev']

