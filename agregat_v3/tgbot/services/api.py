import asyncio
import aiohttp
import json
import logging
import requests


def write_to_file(text, filename, encoding="utf-8"):
    # open the file with write mode
    with open(filename, "w", encoding=encoding) as f:
        # write the text to the file
        f.write(text)


async def register_new_product_and_user(
    phone_number, media_files, datetime, got_data: dict, categories=[], status="1"
):
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

    payload = json.dumps(
        {
            "product_user": {
                "user_id": int(got_data["user_id"]),
                "user_name": f"{got_data['user_name']}",
                "user_link": f"{got_data['user_link']}",
                "phone_number": f"{phone_number}",
            },
            "category": list(categories),
            "group": {
                "group_id": int(got_data["group_id"]),
                "group_name": f"{got_data['group_name']}",
                "group_link": f"{got_data['group_link']}",
            },
            "message_id": int(got_data["message_id"]),
            "message_text": f"{got_data['message_text']}",
            "media_file": f"{media_files}",
            "datatime": datetime,
            "status": status,
        }
    )
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            logging.critical("product added")
            try:
                logging.error(await response.json())
                return await response.json()
            except:
                write_to_file(await response.text(), "last_error.txt")
                logging.critical("An CRITICAL error occured while adding product")


async def delete_product(message_id, group_id):
    url = f"http://62.209.129.42/product/?group_id={group_id}&message_id={message_id}"

    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            logging.critical("product deleted")
            return response.status


async def get_product(group_id, message_id):
    url = f"http://62.209.129.42/product/?group_id={group_id}&message_id={message_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            logging.critical("product fetched")
            return await response.json()


async def update_product(message_id, group_id, categories: list):
    url = f"http://62.209.129.42/update_by_group_id/?group_id={group_id}&message_id={message_id}"
    payload = json.dumps({"category": categories})
    headers = {"Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, data=payload) as response:
            logging.critical("product updated")
            return await response.json()
