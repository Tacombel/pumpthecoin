import requests
import sys
from config import Config

def send_telegram_msg(message):
    bot_token = Config.telegram_token
    bot_chatID = Config.user_id
    bot_message = message
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=html&text=' + bot_message
    print(send_text)
    response = requests.get(send_text)
    return response.json()

if __name__ == "__main__":
    message = sys.argv[1]
    print(send_telegram_msg(message))
