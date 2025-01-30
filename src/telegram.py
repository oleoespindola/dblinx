import os

import requests

import json

# Your bot token
BOT_TOKEN = os.getenv('telegram_token')
CHAT_ID = os.getenv('chat_id')

class Telegram:
    def __init__(self, message: str):
        print(f'try send message error: {message}')
        self.message = message
        self.send()

    def send(self):
        URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            'text': f'dblinx | ' + self.message,
            'chat_id': CHAT_ID,
        }

        response = requests.post(URL, json=payload)

        print(f'\nError report sent via telegram with status code {response.status_code}')