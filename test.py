import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# The first parameter is the .session file name (absolute paths allowed)
client = TelegramClient('agregat', API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def my_event_handler(event):
    print(event.chat_id)

client.start()
client.run_until_disconnected()