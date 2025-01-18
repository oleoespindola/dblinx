import os

import requests

import json

# Your bot token
BOT_TOKEN = os.getenv('telegram_token')

class Telegram:
    def __init__(self, message: str):
        print(f'try send message error: {message}')
        self.message = message
        self.send()

    def send(self):
        URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            'text': self.message,
        }

        with open('./json/chat_IDs.json', 'r') as file:
            chat_IDs = json.load(file)['chat_IDs']

        for chat_ID in chat_IDs:
            payload.update({
                'chat_id': chat_ID,
            })

            response = requests.post(URL, json=payload)

            print(response.json())