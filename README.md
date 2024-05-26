## Telegram bot for sending notifications

This bot sends a notification to the user in Telegram if its work has been verified.

## Launch

Download the code from [Github](https://github.com/Sharipat/dvmn-telegram-bot)

Install dependencies with the command

```
  pip install -r requirements.txt
  ```

In the root of the folder, create a file ```.env```, in which write

``` AUTH_TOKEN ``` - your token for authorization on [Devman](https://dvmn.org/api/docs/)

```TOKEN``` - your bot token from [BotFather](https://telegram.me/BotFather)

``` CHAT_ID ``` - ID for chat with the bot [userinfobot](https://telegram.me/userinfobot)

Launch the site with the command
  ```
   python3 script.py
  ```


## Example notifications

  ![screenshot](/screenshot-bot.png)

## Project goals

The code is written for educational purposes - this is a lesson in the course on Python and web development on the site [Devman](https://dvmn.org).