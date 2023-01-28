import os
from traceback import print_exc
from dotenv import load_dotenv
from telethon import TelegramClient, events
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# The first parameter is the .session file name (absolute paths allowed)
client = TelegramClient('agregat', API_ID, API_HASH)

@client.on(events.Album(chats=-861607927, blacklist_chats=True))
async def albums(event):
    await event.forward_to(-861607927)
    raise events.StopPropagation



@client.on(events.NewMessage(incoming=True, chats=-861607927, blacklist_chats=True))
async def my_event_handler(event):
    if event.is_private:
        user = await client.get_entity(event.peer_id)
        first = user.first_name
        last = user.last_name if not "None" else ""
        await client.send_message(-861607927, f"Сообщение с пользователя {first} {last}")
        # if await event.media:
        #     await client.send
        await event.forward_to(-861607927)
        print('it\'s  a user')
    else:
        group = await client.get_entity(event.peer_id)
        try:
            user = await client.get_entity(event.from_id)        
            first = user.first_name
            last = user.last_name if not "None" else ""
            link=f"{first} {last}"
        except:
            print_exc()
            link = "username"
        try:
            link = f"<a href=https://t.me/+{user.phone}>{first} {last}</a>"
        except:
            try:
                link = f"<a href=https://t.me/{user.username}>{first} {last}</a>"
            except:
                pass
        group_link = f'{group.title}'
        try:
            group_link = f'<a href=https://t.me/{group.username}>{group.title}</a>'
        except:
            pass
        if event.message.text and event.message.media == None:
            await client.send_message(-861607927, f"Сообщение от пользователя {link}, группы {group_link}\n{event.message.text}", parse_mode="Html")
        elif event.message.media:
            print(event.message.photo)
            await client.send_message(-861607927, f"Сообщение от пользователя {link}, группы {group_link}", parse_mode="Html")      

    raise events.StopPropagation

    
    

client.start()
client.run_until_disconnected()