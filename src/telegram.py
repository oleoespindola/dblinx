import os

import requests

import json

# Your bot token
BOT_TOKEN = os.getenv('telegram_token')

class Telegram:
    def __init__(self, message: str):
        self.message = message
        self.send()

    def send(self):
        URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            'message': self.message,
        }

        with open('.\\json\\tel_usrers.json', 'r') as file:
            tel_users = json.load(file)['phone_numbers']

        for users in tel_users:
            payload.update({
                'phone_number': users,
            })

            response = requests.post(URL, json=payload)

            print(response.json())