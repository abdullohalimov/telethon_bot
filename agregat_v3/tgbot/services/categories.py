# Import requests library to send HTTP requests
import difflib
import json
def get_categories(response, txtmsg, coef: float):
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        data = dict(json.loads(response.content))
        a = data['data']
        categories = dict()
        parents = dict()
        for i in a:
            for j in i["child_categories"]:
                cat_id = j["id"]
                cat_name = j["name"]
                parents[cat_id] = cat_name
                if len(j["child_categories"]) == 0:
                    parent_cat = i["id"]
                    # parent_cat = i["name"]
                    if categories.get(parent_cat) is None:
                        categories[parent_cat] = list()
                        categories[parent_cat].append({j['id']: j['name']})
                    else:
                        categories[parent_cat].append({j['id']: j['name']})
                else:
                    categories[cat_id] = list()
                    for e in j["child_categories"]:
                        categories[cat_id].append({e["id"]: e["name"]})
        # print(parents)
        categories2 = set()
        for key, value in categories.items():
            for j in value:
                str1 = txtmsg.lower().split()
                str2 = list(j.values())[0].lower()
                # print(key, value)
                a = difflib.get_close_matches(str2, str1, 3, coef) 
                for i in a:
                    # categories2.add(f"{key}||{list(j.keys())[0]}||{parents[key]}||{str2}||{set(a)}")  
                    categories2.add(f'{list(j.keys())[0]}')
        return categories2
    else:
        # Handle the error if the response status code is not 200 (OK)
        print("Error: ", response.status_code)
        return None
    

'''
if response.status_code == 200:
        data = dict(json.loads(response.content))
        a = data["data"]
        categories = dict()
        for i in a:
            for j in i["child_categories"]:
                cat_id = j["id"]
                # cat_id = j["name"]
                
                if len(j["child_categories"]) == 0:
                    parent_cat = i["id"]
                    # parent_cat = i["name"]
                    if categories.get(parent_cat) is None:
                        categories[parent_cat] = list()
                        categories[parent_cat].append({j['id']: j['name']})
                    else:
                        categories[parent_cat].append({j['id']: j['name']})
                else:
                    categories[cat_id] = list()
                    for e in j["child_categories"]:
                        categories[cat_id].append({e["id"]: e["name"]})
'''


"""
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
            # for i in response.json()['data']:
            #     print(i['name'], i['id'])

            return response.json()['data']
        else:
            url = f'https://aztester.uz/api-announcement/v1/category?category_id={catalog}'
            response = requests.request("GET", url, headers=headers, data=payload)
            # for i in response.json()['data'][0]['child_categories']:
            #     print(i['name'], i['id'])

            return response.json()['data'][0]['child_categories']
    else:
        url = f"https://aztester.uz/api-announcement/v1/category/breadcrumb?categories={c}"
        response = requests.request("GET", url, headers=headers, data=payload)
        #pprint(response.json()['data']['categories'][0])

        category_id = response.json()['data']['categories'][0]['category_id']
        name = f"{response.json()['data']['categories'][0]['name']}"

        aa = ''
        try:
            aa = get_catalog(c=category_id)
        except: pass

        cat = f"{name}:>:{category_id}:>:{aa}"
        if category_id == None:
            return name
        else:
            return cat"""