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
    print(event.peer_id)
    try:
        if event.peer_id.user_id != None:
            await event.forward_to(-835631089)
            await client.send_message(-835631089, 'it\'s from a user')
            print('it\'s  a user')
    except: 
        try:
            if event.peer_id.chat_id != None:
                await event.forward_to(-835631089)
                await client.send_message(-835631089, 'it\'s from a group')
                print("It's from a chat ")
        except:
            try:
                if event.peer_id.channel_id != None:
                    await event.forward_to(-835631089)
                    await client.send_message(-835631089, 'it\'s from a channel')
                    print("It's from a channel")
            except:
                pass

    
    

client.start()
client.run_until_disconnected()