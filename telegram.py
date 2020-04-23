import requests
import os
from dotenv import load_dotenv

'''
    Create your telegram bot using TG bot godfather
'''
load_dotenv(verbose=True)
telegram_api_key = os.getenv("TELEGRAM_API_KEY", "")
user_id = os.getenv("TELEGRAM_USER_KEY", "")

def get_received_msg():
    if len(telegram_api_key) > 0:
        url = 'https://api.telegram.org/bot{}/getUpdates'.format(telegram_api_key)
        res = requests.post(url)
        return res.json()

    return {'ok': False}

def send_msg(msg, parse_mode=None):
    if len(telegram_api_key) > 0 and len(user_id) > 0:
        url = 'https://api.telegram.org/bot{}/sendMessage'.format(telegram_api_key)
        data = {'chat_id': user_id, 'text': msg }
        if parse_mode != None:
            data['parse_mode'] = parse_mode

        res = requests.post(url, data)

        return res.json()
    return {'ok': False}
    
if __name__ == "__main__":
    print(send_msg('ping'))

