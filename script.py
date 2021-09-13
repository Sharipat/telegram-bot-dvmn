import logging
import os
import time
from logging.handlers import RotatingFileHandler

import requests
import telegram
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, chat_id, bot_token):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = telegram.Bot(bot_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_response_json(dvmn_token, timestamp):
    url = 'https://dvmn.org/api/long_polling/'
    send_token = 'Token {}'.format(dvmn_token)
    headers = {
        'Authorization': send_token}
    params = {'timestamp': timestamp}
    response = requests.get(url, headers=headers, params=params, timeout=90)
    response.raise_for_status()
    return response.json()


def send_result_messages(chat_id, tg_bot, new_attempts):
    lesson_info = new_attempts[0]
    lesson_title = lesson_info['lesson_title']
    lesson_url = lesson_info['lesson_url']
    tg_bot.send_message(
        text='''
        У вас проверили работу "{}"! 
        Посмотреть результат проверки можно по ссылке https://dvmn.org{}#review-tab
        '''.format(lesson_title, lesson_url),
        chat_id=chat_id)
    if lesson_info['is_negative']:
        tg_bot.send_message(text='К сожалению, в работе нашлись ошибки.', chat_id=chat_id)
    else:
        tg_bot.send_message(text='Преподавателю все понравилось, можно приступать к следующему уроку!', chat_id=chat_id)


def main():
    load_dotenv()
    chat_id = os.getenv('CHAT_ID')
    bot_token = os.getenv('TOKEN')
    dvmn_token = os.getenv('AUTH_TOKEN')
    tg_bot = telegram.Bot(bot_token)
    logging.basicConfig(level=logging.DEBUG)
    telegram_handler = TelegramLogsHandler(chat_id, bot_token)
    handler = RotatingFileHandler("app.log", maxBytes=200, backupCount=2)
    logger.addHandler(telegram_handler)
    logger.addHandler(handler)
    timestamp = None
    logger.info('Бот запущен')
    while True:
        try:
            json_response = get_response_json(dvmn_token, timestamp)
            if json_response['status'] == 'timeout':
                timestamp = json_response['timestamp_to_request']
            else:
                timestamp = json_response['last_attempt_timestamp']
                new_attempts = json_response['new_attempts']
                send_result_messages(chat_id, tg_bot, new_attempts)
                logger.debug('Отправлено сообщение от бота')
        except requests.exceptions.ReadTimeout:
            continue
        except requests.ConnectionError:
            logger.error('Проблемы с соединением')
            time.sleep(30)
        except Exception:
            logging.exception()


if __name__ == '__main__':
    main()
