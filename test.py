import requests
import json

url = "http://62.209.129.42/product/"

payload = json.dumps({
  "product_user": {
    "user_id": "6006111111",
    "user_name": "JobirTest",
    "user_link": "@jobir_umirov",
    "phone_number": "+998900426898"
  },
  "categories": [
    750,
    751
  ],
  "group": {
    "group_id": -1001763109000,
    "group_name": "Test",
    "group_link": "https://t.me/Tes"
  },
  "message_id": 100,
  "message_text": "Товук патини тозалидиган барабан резиналари сотилади сифатли махсулоти озимизикиям бор+998990017817. +998909079441",
  "media_file": "AgACAgIAAxkBAAIRfWQew6PFEYSHKiGV0OXFYNZRghI4AAJ9yjEbZPOgSCqjC4wkKJMoAQADAgADeQADLwQ,AgACAgIAAxkBAAIRfmQew6PNSVMflD0ic7K5fpYeDXwJAAJ_yjEbZPOgSEwKA7w92P-0AQADAgADeQADLwQ",
  "datetime": "2023-05-28T18:16:41+05:00"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
