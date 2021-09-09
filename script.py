import requests
import telegram
import os
from dotenv import load_dotenv


def get_response_json(dvmn_token, timestamp):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {dvmn_token}'}
    params = {'timestamp': timestamp}
    response = requests.get(url, headers=headers, params=params, timeout=90)
    response.raise_for_status()
    return response.json()


def telegram_bot(chat_id, bot_token, new_attempts):
    bot = telegram.Bot(bot_token)
    lesson_info = new_attempts[0]
    lesson_title = lesson_info['lesson_title']
    lesson_url = lesson_info['lesson_url']
    bot.send_message(
        text=f'У вас проверили работу "{lesson_title}"! \n'
             f'Посмотреть результат проверки можно по ссылке https://dvmn.org{lesson_url}#review-tab',
        chat_id=chat_id)
    if lesson_info['is_negative']:
        bot.send_message(text='К сожалению, в работе нашлись ошибки.', chat_id=chat_id)
    else:
        bot.send_message(text='Преподавателю все понравилось, можно приступать к следующему уроку!')


def main():
    load_dotenv()
    chat_id = os.getenv('CHAT_ID')
    bot_token = os.getenv('TOKEN')
    dvmn_token = os.getenv('AUTH_TOKEN')
    timestamp = None
    while True:
        try:
            json_response = get_response_json(dvmn_token, timestamp)
            if json_response['status'] == 'timeout':
                timestamp = json_response['timestamp_to_request']
            else:
                timestamp = json_response['last_attempt_timestamp']
                new_attempts = json_response['new_attempts']
                telegram_bot(chat_id, bot_token, new_attempts)
        except requests.exceptions.ReadTimeout:
            print('Проверенных работ нет. Повторный запуск бота.')
            continue
        except requests.ConnectionError:
            print('Проблемы с подключением!')


if __name__ == '__main__':
    main()
