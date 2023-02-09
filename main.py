import os
import secrets
import logging
from peewee import *
from types import NoneType
from database import Person
from dotenv import load_dotenv
from telethon import TelegramClient, events

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# The first parameter is the .session file name (absolute paths allowed)
client = TelegramClient('agregat', API_ID, API_HASH)

# @client.on(events.Album(chats=-861607927, blacklist_chats=True))
# async def albums(event):
#     await event.forward_to(-861607927)
#     raise events.StopPropagation



@client.on(events.NewMessage(incoming=True, chats=-1001308294192, blacklist_chats=True))
async def messages_hand(event):
    if event.is_private:
        pass
        # user = await client.get_entity(event.peer_id)
        # first = user.first_name
        # last = user.last_name if not "None" else ""
        # await client.send_message(-861607927, f"Сообщение с пользователя {first} {last}")
        # # if await event.media:
        # #     await client.send
        # await event.forward_to(-861607927)
        # print('it\'s  a user')
        raise events.StopPropagation
    else:
        group = await event.message.get_chat()
        try:
            user = await event.message.get_sender()
            channel = False
            first_name = user.first_name         
            last_name = user.last_name if type(user.last_name) != NoneType else ""
            fullname = f"{first_name} {last_name}"
            print(fullname)
            try:
                if type(user.phone) == NoneType:
                    raise Exception
                link = f"<a href=https://t.me/+{user.phone}>{fullname}</a>"
            except:
                try:
                    if type(user.username) == NoneType:
                        raise Exception

                    link = f"<a href=https://t.me/{user.username}>{fullname}</a>"
                except:
                    link = fullname
        except:
            fullname = user.title
            link = f'<a href=https://t.me/{user.username}>{group.title}</a>'
            channel = True
        
        group_link = f'{group.title}'
        try:
            group_link = f'<a href=https://t.me/{group.username}>{group.title}</a>'
        except:
            pass
        if event.message.text:
            if event.message.media:
                filename=f'{secrets.token_hex(8)}.jpg'
                await event.message.download_media(file=f"media/{filename}")          
                Person.get_or_create(
                user_id=user.id, 
                user_name=fullname, 
                user_link=link, 
                group_id=group.id, 
                group_name=group.title, 
                group_link=group_link, 
                message_text=event.message.text, 
                media_files=filename
                )

            else:
                Person.get_or_create(
                user_id=user.id, 
                user_name=fullname, 
                user_link=link, 
                group_id=group.id, 
                group_name=group.title, 
                group_link=group_link, 
                message_text=event.message.text, 
                media_files='none'
                )
            
            if not channel:
                await client.send_message(-1001308294192, f"Сообщение от пользователя {link}, группы {group_link}\n{event.message.text}", file=event.message.media, parse_mode="Html")
            else:
                await client.send_message(-1001308294192, f"Сообщение от канала {group_link}\n{event.message.text}", file=event.message.media,parse_mode="Html")

    raise events.StopPropagation



    

client.start()
client.run_until_disconnected()