# Doppelgänger Bot

> Still in development

Telegram bot that imitates the user speech pattern.


## How to use

- Get an api_id from Telegram API (https://core.telegram.org/api/obtaining_api_id)
- Create a `config.ini` file:
```
[Telegram]

api_id = [your api_id]
api_hash = [your api_hash]

phone = [your phone number with + country code]
username = [your telegram username]
```
- Download all the dependencies
- Change the `CHAT_IN_1`, `CHAT_IN_2` and `CHAT_OUT` files to your chat IDs
- Run `python3 telegram_history.py`