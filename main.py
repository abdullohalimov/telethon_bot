import regex
from telethon import TelegramClient, events
from dotenv import load_dotenv
from datetime import datetime
from agregat_bot.tgbot.models.database import Person
from types import NoneType
from peewee import *
import os
import logging
import secrets
import requests
from lingua import Language, LanguageDetectorBuilder

# Import json library to parse JSON data
import json
from test1 import get_categories
# Define the URL of the API endpoint
url = "https://aztester.uz/api-announcement/v1/category/tree"



def detect_cyrillic_language(text):
    # languages = [Language.TURKISH, Language.ENGLISH]
    detector = LanguageDetectorBuilder.from_all_languages_with_cyrillic_script().build()
    return detector.detect_language_of(text)


def get_language(text):
    # languages = [Language.TURKISH, Language.ENGLISH]
    detector = LanguageDetectorBuilder.from_all_languages().build()
    if detector.detect_language_of(text) == Language.RUSSIAN:
        return True
    else:
        return False
# Send a GET request to the URL and store the response object
response_uz = requests.get(url, headers={'language': "uz_latn"})
response_cyrl = requests.get(url, headers={'language': "uz_cyrl"})
response_ru = requests.get(url, headers={'language': "ru"})

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
        channel = False
        first_name = user.first_name         
        last_name = user.last_name if type(user.last_name) != NoneType else ""
        fullname = f"{first_name} {last_name}"
        print(fullname)
        try:
            if type(user.phone) == NoneType:
                raise Exception
            link = user.phone
            link2 = f"<a href=https://t.me/+{user.phone}>{fullname}</a>"
        except:
            try:
                if type(user.username) == NoneType:
                    raise Exception

                link = user.username
                link2 = f"<a href=https://t.me/{user.username}>{fullname}</a>"
            except:
                link = 'none'
                link2 = fullname
    except:
        fullname = user.title
        link = user.username
        channel = True
    group_link = f'{group.title}'
    try:
        group_link = group.username
        group_link2 = f'<a href=https://t.me/{group.username}>{group.title}</a>'
    except:
        pass
    # Xabarni filtrlash boshlandi
    # print(event.text)
    # print(event.raw_text)
    await client.send_message(
        5536548536, #output 
        message=event.text, #caption
        file=event.messages, #list of messages
    )
    raise events.StopPropagation




@client.on(events.NewMessage(incoming=True, chats=-1001308294192, blacklist_chats=True))
async def messages_hand(event):
    if event.is_private:
        # print(event.message.id)
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
        if event.message.grouped_id == None:
            # Xabar yuborilgan guruh va foydalanuvchini yoki kanalni aniqlash
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
                    link = user.phone
                    link2 = f"<a href=https://t.me/+{user.phone}>{fullname}</a>"
                except:
                    try:
                        if type(user.username) == NoneType:
                            raise Exception

                        link = user.username
                        link2 = f"<a href=https://t.me/{user.username}>{fullname}</a>"
                    except:
                        link = 'none'
                        link2 = fullname
            except:
                fullname = user.title
                link = user.username
                channel = True
            group_link = f'{group.title}'
            try:
                group_link = group.username
                group_link2 = f'<a href=https://t.me/{group.username}>{group.title}</a>'
            except:
                pass
            # Xabarni filtrlash boshlandi
            if event.message.text and len(event.message.text.split()) > 3:
                if get_language(event.message.text):
                    ctgrs = get_categories(response_ru, event.message.text)
                else:
                    if detect_cyrillic_language(event.message.text):
                        print("Текст на кириллице")
                        ctgrs = get_categories(response_cyrl, event.message.text)

                    else:
                        print("Matn lotinchada")
                        ctgrs = get_categories(response_uz, event.message.text)
                # data = f"""'user_id' :^ {user.id}, \n'user_name' :^ {fullname}, \n'user_link' :^ {link}, \n'group_id' :^ {group.id}, \n'group_name' :^ {group.title}, \n'group_link' :^ {group_link}, \n'message_id' :^ {event.message.id}, \n'message_text' :^ {event.message.text}"""
                data = f"""{user.id}(delimeter){fullname}(delimeter){link}(delimeter){group.id}(delimeter){group.title}(delimeter){group_link}(delimeter){event.message.id}(delimeter){event.message.text}"""
                if ctgrs != "":
                    # try:
                    #     ex_db_record: Person = Person.get(Person.message_text == event.message.text)       
                    #     ex_db_record.datatime = datetime.now()
                    #     ex_db_record.save()
                    # except:
                    #     Person.get_or_create(
                    #     user_id=user.id, 
                    #     user_name=fullname, 
                    #     user_link=link, 
                    #     group_id=group.id, 
                    #     group_name=group.title, 
                    #     group_link=group_link, 
                    #     message_id=event.message.id, 
                    #     message_text=event.message.text, 
                    #     category=ctgrs, 
                    #     media_files='none',
                    #     datatime=datetime.now()
                    #     )
                    
                    if not channel:
                        await client.send_message(-1001308294192, f"Statusi: Bazaga #joylandi\nUser: {link2}\nGroup: {group_link2}\nCatalogs: {ctgrs}\nMessage: {event.message.text}\nmessage_link: https://t.me/{group_link}/{event.message.id}", file=event.message.media, parse_mode="Html", link_preview=False)
                    else:
                        await client.send_message(-1001308294192, f"Statusi: Bazaga #joylandi\nChannel: {group_link2}\nCatalogs: {ctgrs}\nMessage: {event.message.text}\nmessage_link: https://t.me/{group_link}/{event.message.id}", file=event.message.media,parse_mode="Html", link_preview=False)
                    
                    
                    # await client.send_message(5536548536, f"{user.id}(delimeter){fullname}(delimeter){link}(delimeter){group.id}(delimeter){group.title}(delimeter){group_link}(delimeter){event.message.id}(delimeter){event.message.text}(delimeter){ctgrs}(delimeter){'none'}(delimeter){datetime.now()}(delimeter)#joylanmadi", file=event.message.media, parse_mode="Html", link_preview=False)



                else:
                    if not channel:
                        await client.send_message(-1001308294192, f"Statusi: Bazaga #joylanmadi\nUser {link2}\nGroup {group_link2}\nmessage: {event.message.text}\nmessage_link: https://t.me/{group_link}/{event.message.id}", file=event.message.media, parse_mode="Html", link_preview=False)
                    else:
                        await client.send_message(-1001308294192, f"Statusi: Bazaga #joylanmadi\nСообщение от канала {group_link2}\nMessage:{event.message.text}\nmessage_link: https://t.me/{group_link}/{event.message.id}", file=event.message.media,parse_mode="Html", link_preview=False)
                    # await client.send_message(5976776249, str(data))
                    # await event.message.forward_to(5536548536)
                await client.send_message("@Testfordifferentlibraries_bot", data, file=event.message.media, parse_mode="Html", link_preview=False)
                
                # if event.message.media:
                #     filename=f'{secrets.token_hex(8)}{event.message.file.ext}'
                #     await event.message.download_media(file=f"media/{filename}") 
                    # await client.send_message(5536548536, str(data), file=event.message.media)
                    
                    # try:
                    #     ex_db_record: Person = Person.get(Person.message_text == event.message.text)       
                    #     ex_db_record.datatime = datetime.now()
                    #     ex_db_record.save()
                    # except:
                    #     Person.get_or_create(
                    #     user_id=user.id, 
                    #     user_name=fullname, 
                    #     user_link=link, 
                    #     group_id=group.id, 
                    #     group_name=group.title, 
                    #     group_link=group_link, 
                    #     message_id=event.message.id, 
                    #     message_text=event.message.text, 
                    #     category=ctgrs, 
                    #     media_files=filename,
                    #     datatime=datetime.now()
                    #     )

        raise events.StopPropagation

    

client.start()
client.run_until_disconnected()