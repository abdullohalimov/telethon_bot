import requests
import json
from pprint import pprint

def get_catalog(catalog = 0, lan = 'uz_latn', c = ''):
    payload={}
    headers = {
        'content-type': 'application/json',
        'lan': f'{lan}'
    }

    if c == '':
        if catalog == 0:
            url = "https://aztester.uz/api-announcement/v1/category/tree"
            response = requests.request("GET", url, headers=headers, data=payload)
            categoires = dict()
            for i in response.json()['data']:
                print(i['name'], i['id'])
                categoires[i['id']] = i['name']

            # return response.json()['data']
            return categoires
        else:
            url = f'https://aztester.uz/api-announcement/v1/category?category_id={catalog}'
            response = requests.request("GET", url, headers=headers, data=payload)
            categoires = dict()
            for i in response.json()['data'][0]['child_categories']:
                print(i['name'], i['id'])
                categoires[i['id']] = i['name']

            # return response.json()['data'][0]['child_categories']
            return categoires
    else:
        url = f"https://aztester.uz/api-announcement/v1/category/breadcrumb?categories={c}"
        response = requests.request("GET", url, headers=headers, data=payload)
        #pprint(response.json()['data']['categories'][0])

        category_id = response.json()['data']['categories'][0]['category_id']
        category_id2 = response.json()['data']['categories'][0]['id']
        name = f"{response.json()['data']['categories'][0]['name']}"

        aa = ''
        try:
            aa = get_catalog(c=category_id)
        except: pass

        cat = f"{name}:>:{category_id2}:>:{aa}"
        if category_id == None:
            return name
        else:
            return cat
        
# pprint(get_catalog(818, 'uz_latn', ''))