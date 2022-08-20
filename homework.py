import logging
import os
import sys

import requests
import time

from dotenv import load_dotenv

# заводим логер
logger = logging.getLogger()
streamHandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


# Забираем секреты из окружения
load_dotenv()
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    pass


def get_api_answer(current_timestamp):
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = request.get(ENDPOINT, headers=HEADERS, params=params)


def check_response(response):
    params = {'from_date': time.time()}
    



def parse_status(homework):
    homework_name = ...
    homework_status = ...

    verdict = ...

    ...

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    '''Провенряет наличие секретов'''
    if PRACTICUM_TOKEN is None:
        logging.critical('Не удалось найти токен Практикума')
        return False
    elif TELEGRAM_TOKEN is None:
        logging.critical('Не удалось найти токен Telegram')
        return False
    elif TELEGRAM_CHAT_ID is None:
        logging.critical('Не удалось найти id чата пользователя')
        return False
    return True


def main():
    """Основная логика работы бота."""

    ...

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    ...

    while True:
        try:
            response = ...

            ...

            current_timestamp = ...
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
            time.sleep(RETRY_TIME)
        else:
            ...


if __name__ == '__main__':
    main()
