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

        with open('phoen_numbers.json', 'r') as file:
            phone_numbers = json.load(file)['phone_numbers']

        for number in phone_numbers:
            payload.update({
                'phone_number': number,
            })

            response = requests.post(URL, json=payload)

            print(response.json())