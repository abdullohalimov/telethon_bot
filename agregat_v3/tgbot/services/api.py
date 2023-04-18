import asyncio
import aiohttp
import json

import requests


async def register_new_product_and_user(phone_number, media_files, datetime, got_data: dict, categories=[], status="1"):
    """
    Registers a new product and user along with their information.

    Args:
        got_data (dict): A dictionary containing user and group information.
        phone_number (str): The phone number of the user.
        categories (list): A list of categories for the product.
        media_files (str): The name(s) of the media file(s).
        datetime (str): The date and time of the product registration.
        status (str, optional): The status of the registration. Defaults to "1".

    Returns:
        None
    """
    url = "http://62.209.129.42/product/"

    payload = json.dumps({
    "product_user": {
        "user_id": int(got_data['user_id']),
        "user_name": f"{got_data['user_name']}",
        "user_link": f"{got_data['user_link']}",
        "phone_number": f"{phone_number}"
    },
    "category": list(categories),
    "group_id": int(got_data['group_id']),
    "group_name": f"{got_data['group_name']}",
    "group_link": f"{got_data['group_link']}",
    "message_id": int(got_data['message_id']),
    "message_text": f"{got_data['message_text']}",
    "media_file": f"{media_files}",
    "datatime": datetime,
    "status": status,
    })
    headers = {
    'Content-Type': 'application/json'
    }
    print(payload)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            print(await response.text())

async def delete_product(message_id, group_id):
    url = f"http://62.209.129.42/product/?group_id={group_id}&message_id={message_id}"

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            print(await response.text())


async def get_product(group_id, message_id):
    url = f"http://62.209.129.42/product/?group_id={group_id}&message_id={message_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


def update_product(phone_number, group_id, message_id, got_data: dict, categories=[], media_files="", datetime="", status="1", ):
    url = f"http://62.209.129.42/update_by_group_id/?group_id={group_id}&message_id={message_id}"

    payload = json.dumps({
    "product_user": {
        "user_id": int(got_data['user_id']),
        "user_name": f"{got_data['user_name']}",
        "user_link": f"{got_data['user_link']}",
        "phone_number": f"{phone_number}"
    },
    "category": list(categories),
    "group_id": int(got_data['group_id']),
    "group_name": f"{got_data['group_name']}",
    "group_link": f"{got_data['group_link']}",
    "message_id": int(got_data['message_id']),
    "message_text": f"{got_data['message_text']}",
    "media_file": f"{media_files}",
    "datatime": datetime,
    "status": status,
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)


# asyncio.run(delete_product())
# async def







