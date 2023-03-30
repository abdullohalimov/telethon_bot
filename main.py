import regex
from telethon import TelegramClient, events
from dotenv import load_dotenv
from types import NoneType
from peewee import *
import os
import logging

# Import json library to parse JSON data
from test1 import get_categories
# Define the URL of the API endpoint

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# The first parameter is the .session file name (absolute paths allowed)
client = TelegramClient('agregat', API_ID, API_HASH)

@client.on(events.Album())
async def handler(event):
    # Xabar yuborilgan guruh va foydalanuvchini yoki kanalni aniqlash
    # print(event)
    group = await event.original_update.message.get_chat()
    try:
        user = await event.original_update.message.get_sender()
        first_name = user.first_name         
        last_name = user.last_name if type(user.last_name) != NoneType else ""
        fullname = f"{first_name} {last_name}"
        print(fullname)
        try:
            if type(user.phone) == NoneType:
                raise Exception
            link = user.phone
        except:
            try:
                if type(user.username) == NoneType:
                    raise Exception

                link = user.username
            except:
                link = 'none'
    except:
        fullname = user.title
        link = user.username
    group_link = f'{group.title}'
    try:
        group_link = group.username
    except:
        pass
    # Xabarni filtrlash boshlandi

    data = f"""{user.id}(delimeter){fullname}(delimeter){link}(delimeter){group.id}(delimeter){group.title}(delimeter){group_link}(delimeter){event.original_update.message.id}(delimeter){event.original_update.message.text}"""
    if not user.bot:
        await client.send_message(
            "@Testfordifferentlibraries_bot", #output 
            message=data, #caption
            file=event.messages, #list of messages
        )
        raise events.StopPropagation




@client.on(events.NewMessage(incoming=True, chats=-1001308294192, blacklist_chats=True))
async def messages_hand(event):
    if event.is_private:
        pass
        raise events.StopPropagation
    else:
        if event.message.grouped_id == None:
            # Xabar yuborilgan guruh va foydalanuvchini yoki kanalni aniqlash
            group = await event.message.get_chat()
            try:
                user = await event.message.get_sender()
                first_name = user.first_name         
                last_name = user.last_name if type(user.last_name) != NoneType else ""
                fullname = f"{first_name} {last_name}"
                print(fullname)
                try:
                    if type(user.phone) == NoneType:
                        raise Exception
                    link = user.phone
                except:
                    try:
                        if type(user.username) == NoneType:
                            raise Exception

                        link = user.username
                    except:
                        link = 'none'
            except:
                fullname = user.title
                link = user.username
            group_link = f'{group.title}'
            try:
                group_link = group.username
            except:
                pass
            # Xabarni filtrlash boshlandi
            if event.message.text and len(event.message.text.split()) > 3:
                if not user.bot:
                    data = f"""{user.id}(delimeter){fullname}(delimeter){link}(delimeter){group.id}(delimeter){group.title}(delimeter){group_link}(delimeter){event.message.id}(delimeter){event.message.text}"""
                    
                    await client.send_message("@Testfordifferentlibraries_bot", data, file=event.message.media, parse_mode="Html", link_preview=False)
                


        raise events.StopPropagation

    
client.start()
client.run_until_disconnected()