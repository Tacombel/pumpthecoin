import requests
import os
import logging

LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler()
c_handler.setLevel(LOGLEVEL)
c_format = logging.Formatter('%(asctime)s %(levelname)s %(name)s : %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)
logger.setLevel(LOGLEVEL)

logger.info(f'LOGLEVEL: {LOGLEVEL}')

def send_telegram_msg(message):
    logging.debug(f'----------send_telegram_msg----------')
    bot_token = os.getenv('TELEGRAM_TOKEN')
    logging.debug(f'TELEGRAM_TOKEN: {bot_token}')
    chat_ID = os.getenv('CHAT_ID')
    logging.debug(f'CHAT_ID: {chat_ID}')
    bot_message = message
    logging.debug(f'bot_message: {bot_message}')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_ID + '&parse_mode=html&text=' + bot_message
    # El signo # necesita ser substituido porque si no urllib corta la uri
    send_text = send_text.replace('#', '%23')
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
