import requests

class Proxys:
    def __init__(self):
        
        self.token = '7495324692:AAEe7zZUTVhLkSRC6TRPb5aZmkoVWDeBwiI'
        self.chat_id = '5487978588'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
