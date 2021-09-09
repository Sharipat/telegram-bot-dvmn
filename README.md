## Телеграм бот для отправки уведомлений

Данный бот отправляет пользователю уведомление в Телеграм, если его работа была проверена.

## Запуск

Скачайте код с [Github](https://github.com/Shirlusha/dvmn-telegram-bot)

Установите зависимости командой

```
 pip install -r requirements.txt
 ```

В корне папки создайте файл ```.env```, в который впишите

``` AUTH_TOKEN ``` - ваш токен для авторизации на [Девман](https://dvmn.org/api/docs/)

```TOKEN``` - токен вашего бота от [BotFather](https://telegram.me/BotFather)

``` CHAT_ID  ``` - ID для чата с ботом [userinfobot](https://telegram.me/userinfobot)

Запустите сайт командой
 ```
  python3 script.py
 ```


## Пример уведомлений

 ![screenshot](/screenshot-bot.png)

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
