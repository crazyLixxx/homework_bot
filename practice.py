import http
import logging
import os
import sys

import requests
import time

from telegram import Bot

from dotenv import load_dotenv

from exceptions import (
    HomeworkIsntADicException,
    GetNoAnswerException,
    GetNot200AnswerException,
    NoHomeworksInAnswerException,
    NotDocumentedStatusException,
    NoDictInApiAnsewerException,
    NotEnouthSecrets,
)

# Заводим логер
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


# Взводим бота
bot = Bot(token=TELEGRAM_TOKEN)


RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def parse_status(homework: dict) -> str:
    """Получаем статус конкретной домашней работы."""
    logging.debug('Начинаем проверку статуса домашки')
    if isinstance(homework, dict):
        try:
            homework_name = homework.get('homework_name')
            homework_status = homework.get('status')
            verdict = HOMEWORK_STATUSES[homework_status]
            logging.debug('Статус домашки найден, сообщение готово')
            return f'Изменился статус проверки работы "{homework_name}". {verdict}'
        except KeyError:
            logging.error(
                f'Обнаружен недокументированный статус {homework_status}'
            )
            raise NotDocumentedStatusException()
    logging.error('Домашка не в словаре')
    raise HomeworkIsntADicException()



message = {
        "id":124,
        "status":"rejected",
        "homework_name":"username__hw_python_oop.zip",
        "reviewer_comment":"Код не по PEP8, нужно исправить",
        "date_updated":"2020-02-13T16:42:47Z",
        "lesson_name":"Итоговый проект"
}

print(parse_status(message))
