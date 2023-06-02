import requests
import os

def send_telegram_msg(message):
    bot_token = os.getenv('TELEGRAM_TOKEN')
    chatID = os.getenv('USER_ID')
    bot_message = message
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chatID + '&parse_mode=html&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    load_dotenv()
    print(os.getenv('TELEGRAM_TOKEN'))
    message = sys.argv[1]
    print(send_telegram_msg(message))
