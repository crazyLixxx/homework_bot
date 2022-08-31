import http
import logging
import os
import telegram
import sys

import requests
import time

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
streamHandler.setLevel(logging.DEBUG)
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

def send_message(bot: telegram.Bot, message: str) -> None:
    """Если статус домашки изменился - отправляем в тг."""
    logging.debug('Начинаю отправку стаутса в тг')
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info(f'В чат пользователя отправлено сообщение: {message}')
    except Exception as error:
        logging.error(f'Не могу отправить сообщение в тг: {error}')


def get_api_answer(current_timestamp: int) -> dict:
    """Проверяем работоспособность api и возвращаем ответ словарём."""
    logging.debug('Пробуем получить ответ от апи Практикума')
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}

    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        logging.debug('Достучались до апи, получили ответ')
    except Exception as error:
        logging.error(f'Ошибка при запросе к апи Практикума: {error}')
        raise GetNoAnswerException()

    if response.status_code != http.HTTPStatus.OK:
        logging.error('api отдаёт отличный от 200 код')
        raise GetNot200AnswerException()
    else:
        logging.debug('Ответ апи получен и может быть сконвертирован')
        return response.json()

def check_response(response: dict) -> list:
    """Проверяем корректность ответа api и возвращем домашние работы."""
    logger.debug('Начало проверки корректности ответа апи')
    if isinstance(response, dict):
        try:
            homeworks = response['homeworks']
            logger.debug('Апи содержит корректный ответ')
            return homeworks
        except KeyError:
            logger.error('В апи нет списка статусов домашних работ')
            raise NoHomeworksInAnswerException()
    else:
        logger.error('Апи вернуло не словарь')
        raise NoDictInApiAnsewerException()
 

def parse_status(homework: dict) -> str:
    """Получаем статус конкретной домашней работы."""
    logging.debug('Начинаем проверку статуса домашки')
    if isinstance(homework, dict):
        try:
            homework_name = homework.get('homework_name')
            homework_status = homework.get('status')
            verdict = HOMEWORK_STATUSES[homework_status]
            logging.debug('Статус домашки найден, сообщение готово')
            return (
                f'Изменился статус проверки работы "{homework_name}". {verdict}'
            )
        except KeyError:
            logging.error(
                f'Обнаружен недокументированный статус {homework_status}'
            )
            raise NotDocumentedStatusException()
    logging.error('Домашка не в словаре')
    raise HomeworkIsntADicException()


def check_tokens() -> bool:
    """Провенряет наличие секретов."""
    logger.debug('Начало проверки наличия секретов')
    if PRACTICUM_TOKEN is None:
        logging.critical('Не удалось найти токен Практикума')
        raise NotEnouthSecrets()
    elif TELEGRAM_TOKEN is None:
        logging.critical('Не удалось найти токен Telegram')
        raise NotEnouthSecrets()
    elif TELEGRAM_CHAT_ID is None:
        logging.critical('Не удалось найти id чата пользователя')
        raise NotEnouthSecrets()
    logger.debug('Все секреты на месте')
    return True


def main() -> bool:
    """Основная логика работы бота."""

    logging.debug('начинаем работу основной функции')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    cached_error = ''
    check_tokens()

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if len(homeworks) > 0:
                for homework in homeworks:
                    message = parse_status(homework)
                    send_message(bot, message)
            else:
                logging.debug('Нет новых статусов')
            current_timestamp = response['current_date']
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            if error == cached_error:
                logging.info(f'сбой уже был ранее зафиксирован: {error}')
            else:
                send_message(bot, message)
                cached_error = error
                logging.info(
                    f'уведомили пользователя, ошибку {error} закешировали'
                )
            time.sleep(RETRY_TIME)
        else:
            logging.debug('основная функция успешно завершила работу')


if __name__ == '__main__':
    main()
