# Import requests library to send HTTP requests
import difflib
import json
import logging
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
                    if categories.get(parent_cat) is None:
                        categories[parent_cat] = list()
                        categories[parent_cat].append({j['id']: j['name']})
                    else:
                        categories[parent_cat].append({j['id']: j['name']})
                else:
                    categories[cat_id] = list()
                    for e in j["child_categories"]:
                        categories[cat_id].append({e["id"]: e["name"]})
        categories2 = set()
        for key, value in categories.items():
            for j in value:
                str1 = txtmsg.lower().split()
                str2 = list(j.values())[0].lower()
                a = difflib.get_close_matches(str2, str1, 3, coef) 
                for i in a:
                    # categories2.add(f"{key}||{list(j.keys())[0]}||{parents[key]}||{str2}||{set(a)}")  
                    categories2.add(f'{list(j.keys())[0]}')
        logging.warning(categories2)
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
