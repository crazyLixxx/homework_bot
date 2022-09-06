import http
import logging
import os
import telegram
import sys

import requests
import time

from dotenv import load_dotenv

from exceptions import (
    CantSendMess,
    HomeworkIsntADicException,
    HomeworksIsNtListException,
    GetNoAnswerException,
    GetNot200AnswerException,
    NoHomeworksInAnswerException,
    NoNameInApiAnsewerException,
    NotDocumentedStatusException,
    NoDictInApiAnsewerException
)

# Заводим логер
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


# Забираем секреты из окружения
load_dotenv()
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


RETRY_TIME = 20
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
        logging.info(f'В чат пользователя отправлено сообщение <{message}>')
    except Exception as error:
        logging.error(f'Не могу отправить сообщение в тг: {error}')
        raise CantSendMess('Не могу отправить сообщение в тг')


def get_api_answer(current_timestamp: int) -> dict:
    """Проверяем работоспособность api и возвращаем ответ словарём."""
    logging.debug('Пробуем получить ответ от апи Практикума')
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}

    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        logging.debug('Достучались до апи, получаем ответ')
    except Exception as error:
        logging.error(f'Ошибка при запросе к апи Практикума: {error}')
        raise GetNoAnswerException('Нет ответа от апи')

    if response.status_code != http.HTTPStatus.OK:
        logging.error('api отдаёт отличный от 200 код')
        raise GetNot200AnswerException('Получаем не 200-й')
    else:
        logging.debug('Ответ апи получен и может быть сконвертирован')
        return response.json()


def check_response(response: dict) -> list:
    """Проверяем корректность ответа api и возвращем домашние работы."""
    logger.debug('Начало проверки корректности ответа апи')
    if isinstance(response, dict):
        try:
            homeworks = response['homeworks']
            logger.debug('Апи вернуло домашки')
            if isinstance(homeworks, list):
                logger.debug('И они в списке!')
                return homeworks
            else:
                logger.error('Домашки не в списке(')
                raise HomeworksIsNtListException('Домашки пришли не списком')
        except KeyError:
            logger.error('В апи нет списка статусов домашних работ')
            raise NoHomeworksInAnswerException('Не найдены домашки')
    else:
        logger.error('Апи вернуло не словарь')
        raise NoDictInApiAnsewerException('Из апи пришло нечто вместо словаря')


def parse_status(homework: dict) -> str:
    """Получаем статус конкретной домашней работы."""
    logging.debug('Начинаем проверку статуса домашки')
    if isinstance(homework, dict):
        try:
            homework_name = homework['homework_name']
        except KeyError:
            logging.error('Не найдено название домашки')
            raise NoNameInApiAnsewerException('У домашки нет имени!')
        try:
            homework_status = homework['status']
            verdict = HOMEWORK_STATUSES[homework_status]
            logging.debug('Статус домашки найден, сообщение готово')
            return (
                f'Изменился статус проверки работы "{homework_name}".{verdict}'
            )
        except KeyError:
            logging.error(
                f'Обнаружен недокументированный статус {homework_status}'
            )
            raise NotDocumentedStatusException('Недокументированный статус!')
    else:
        logging.error('Домашка не в словаре')
        raise HomeworkIsntADicException('Домашка не в словаре')


def check_tokens() -> bool:
    """Провенряет наличие секретов."""
    logging.debug('Начинаем проверку секретов')
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main() -> None:
    """Основная логика работы бота."""
    logging.debug('Начинаем работу основной функции')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    cached_error = ''

    if not check_tokens():
        logging.critical('Не нашли какой-то секрет')
        sys.exit()
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if len(homeworks) > 0:
                for homework in homeworks:
                    message = parse_status(homework)
                    send_message(bot, message)
            else:
                logging.debug('Новых статусов нет')
            current_timestamp = response['current_date']
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            if message == cached_error:
                logging.info(f'Сбой уже был ранее зафиксирован: {error}')
            else:
                send_message(bot, message)
                cached_error = message
                logging.info('Уведомили пользователя, ошибку закэшировали')
            time.sleep(RETRY_TIME)
        else:
            logging.debug('Основная функция будет перезапущена')


if __name__ == '__main__':
    main()
