import requests
import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

base_endpoint = "https://api.skinport.com/v1/"

def get_gloves():
    header = {"Accept-Encoding": "br"}
    search_params ={"app_id":730, "currency":"USD", "tradable":"true"}
    url = base_endpoint + "items"
    res = requests.get(url, params=search_params, headers=header)

    items = res.json() #gets the items from response
    gloves = [] #empty list for storing gloves

    GLOVES = [ # all types of gloves in cs
        "Sports Gloves",
        "Driver Gloves",
        "Hand Wraps",
        "Specialist Gloves",
        "Moto Gloves",
        "Bloodhound Gloves",
        "Hydra Gloves",
        "Broken Fang Gloves"
    ]

    for item in items:
        if any(glove in item["market_hash_name"] for glove in GLOVES):
            gloves.append(item)

    return gloves

def get_price_history():
    gloves = get_gloves()
    gloves_name = []

    for glove in gloves:
        gloves_name.append(glove["market_hash_name"])

    name_lists = ",".join(gloves_name[:3])

    header = {"Accept-Encoding": "br"}
    search_params ={"market_hash_name": name_lists, "app_id":730, "currency":"USD"}
    url = base_endpoint + "sales/history"
    res = requests.get(url, params=search_params, headers=header)

    print(res.json())

get_price_history()