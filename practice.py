import http
import logging
import os
import sys
import time

import requests

from dotenv import load_dotenv

from exception_set import PractikumApiNotOKException

# заводим логер
logger = logging.getLogger()
streamhandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)


# забираем секреты из окружения
load_dotenv()
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/1'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def get_api_answer(current_timestamp):
    '''Проверяем работоспособность api и возвращаем ответ словарём'''
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}

    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception as error:
        logging.error(f'Ошибка при запросе к апи Практикума: {error}')

    if response.status_code != http.HTTPStatus.OK:
        logging.error('api отдаёт отличный от 200 код')
        raise PractikumApiNotOKException()
    else:
        return response.json()

print(get_api_answer(int(time.time())))
