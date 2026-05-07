import requests
import sqlite3
import datetime

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS gloves (
               market_hash_name TEXT UNIQUE,
               currency TEXT,
               last_24h_min REAL,
               last_24h_max REAL,
               last_24h_avg REAL,
               last_24h_median REAL,
               last_24h_vol INTEGER,
               last_7d_min REAL,
               last_7d_max REAL,
               last_7d_avg REAL,
               last_7d_median REAL,
               last_7d_vol INTEGER,
               last_30d_min REAL,
               last_30d_max REAL,
               last_30d_avg REAL,
               last_30d_median REAL,
               last_30d_vol INTEGER,
               last_90d_min REAL,
               last_90d_max REAL,
               last_90d_avg REAL,
               last_90d_median REAL,
               last_90d_vol INTEGER,
               timestamp TEXT UNIQUE
               )""")

connection.commit() 

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

    for item in res.json():
        cursor.execute("""INSERT OR REPLACE INTO gloves VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                       item["market_hash_name"],
                       item["currency"],
                       item["last_24_hours"]["min"],
                       item["last_24_hours"]["max"],
                       item["last_24_hours"]["avg"],
                       item["last_24_hours"]["median"],
                       item["last_24_hours"]["volume"],
                       item["last_7_days"]["min"],
                       item["last_7_days"]["max"],
                       item["last_7_days"]["avg"],
                       item["last_7_days"]["median"],
                       item["last_7_days"]["volume"],
                       item["last_30_days"]["min"],
                       item["last_30_days"]["max"],
                       item["last_30_days"]["avg"],
                       item["last_30_days"]["median"],
                       item["last_30_days"]["volume"],
                       item["last_90_days"]["min"],
                       item["last_90_days"]["max"],
                       item["last_90_days"]["avg"],
                       item["last_90_days"]["median"],
                       item["last_90_days"]["volume"],
                       datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                       ))

    connection.commit()

get_price_history()