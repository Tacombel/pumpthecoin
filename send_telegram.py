import requests
import os
import logging

def send_telegram_msg(message):
    logging.debug(f'----------send_telegram_msg----------')
    bot_token = os.getenv('TELEGRAM_TOKEN')
    logging.debug(f'TELEGRAM_TOKEN: {bot_token}')
    chat_ID = os.getenv('CHAT_ID')
    logging.debug(f'CHAT_ID: {chat_ID}')
    bot_message = message
    logging.debug(f'bot_message: {bot_message}')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_ID + '&parse_mode=html&text=' + bot_message
    logging.debug(f'send_text: {send_text}')
    response = requests.get(send_text)
    logging.debug(f'response: {response}')
    logging.debug(f'----------send_telegram_msg----------')
    return response.json()

if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    load_dotenv()
    print(os.getenv('TELEGRAM_TOKEN'))
    message = sys.argv[1]
    print(send_telegram_msg(message))
