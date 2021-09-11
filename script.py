import os
import time

import requests
import telegram
from dotenv import load_dotenv


def get_response_json(dvmn_token, timestamp):
    url = 'https://dvmn.org/api/long_polling/'
    send_token = 'Token {}'.format(dvmn_token)
    headers = {
        'Authorization': send_token}
    params = {'timestamp': timestamp}
    response = requests.get(url, headers=headers, params=params, timeout=90)
    response.raise_for_status()
    return response.json()


def send_result_messages(chat_id, bot, new_attempts):
    lesson_info = new_attempts[0]
    lesson_title = lesson_info['lesson_title']
    lesson_url = lesson_info['lesson_url']
    bot.send_message(
        text='''
        У вас проверили работу "{}"! 
        Посмотреть результат проверки можно по ссылке https://dvmn.org{}#review-tab
        '''.format(lesson_title, lesson_url),
        chat_id=chat_id)
    if lesson_info['is_negative']:
        bot.send_message(text='К сожалению, в работе нашлись ошибки.', chat_id=chat_id)
    else:
        bot.send_message(text='Преподавателю все понравилось, можно приступать к следующему уроку!', chat_id=chat_id)


def main():
    load_dotenv()
    chat_id = os.getenv('CHAT_ID')
    bot_token = os.getenv('TOKEN')
    dvmn_token = os.getenv('AUTH_TOKEN')
    bot = telegram.Bot(bot_token)
    timestamp = None
    while True:
        try:
            json_response = get_response_json(dvmn_token, timestamp)
            if json_response['status'] == 'timeout':
                timestamp = json_response['timestamp_to_request']
            else:
                timestamp = json_response['last_attempt_timestamp']
                new_attempts = json_response['new_attempts']
                send_result_messages(chat_id, bot, new_attempts)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.ConnectionError:
            time.sleep(30)


if __name__ == '__main__':
    main()
