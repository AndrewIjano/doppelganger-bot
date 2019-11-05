from nltk.tokenize import TweetTokenizer
import random
import pprint
import nltk
import configparser
import json

from telethon.sync import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

CHAT_IN_1 = 1339603030
CHAT_IN_2 = 365932316
CHAT_OUT = 1342903759

# reading configs
config = configparser.ConfigParser()
config.read("config.ini")

# setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

speeches = []
# Create the client and connect

with TelegramClient(username, api_id, api_hash) as client:
    for d in client.iter_dialogs():
        print(d.name, d.entity.id)
    dialogs = client.get_dialogs()

    msgs = client.get_messages(CHAT_IN_1, 8000) \
        + client.get_messages(CHAT_IN_2, 8000)
    for msg in msgs:
        if not msg.out:
            if msg.message is not None:
                speeches += [msg.message.lower()]

print('get messages: OK')


nltk.download('punkt')

sentences = speeches

table = {}

for sentence in sentences:
    words = TweetTokenizer().tokenize(sentence)
    keys = words[:2]
    table.setdefault('#BEGIN', []).append(keys[:])

    for word in words[2:]:
        table.setdefault(tuple(keys), []).append(word)
        keys.pop(0)
        keys += [word]

    table.setdefault('#END', []).append(keys[:][1:])

generated_msgs = []

def generate_msg():
    n = 100
    key = random.choice(table['#BEGIN'])
    # print(key)
    msg = ' '.join(key)

    for _ in range(n):
        new_key = table.setdefault(tuple(key))
        if (new_key == '' or new_key is None):
            break

        new_word = random.choice(new_key)
        if new_word not in [',', '.', ')', '!', '?']:
            msg += ' '
        msg += new_word

        key.pop(0)
        key.append(new_word)

        if (new_word in table['#END']):
            break
    return msg

if input() == 'y':
    with TelegramClient(username, api_id, api_hash) as client:
        @client.on(events.NewMessage(chats=CHAT_OUT))
        async def handler(event):
            msg = generate_msg()
            await client.send_message(CHAT_OUT, msg)
            if len(msg) < 8 or len(msg.split()) < 3:
                await client.send_message(CHAT_OUT, generate_msg())
        client.run_until_disconnected()
