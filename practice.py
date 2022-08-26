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


def send_message(bot: Bot, message: str) -> None:
    """Если статус домашки изменился - отправляем в тг."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as error:
        logging.error(f'Не могу отправить сообщение в тг: {error}')

message = (
    'Изменился статус проверки работы "username__hw_python_oop.zip".'
    'Работа проверена: у ревьюера есть замечания.'
)

send_message(bot, message)
