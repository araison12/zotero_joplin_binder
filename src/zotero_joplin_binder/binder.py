import smtplib
import requests
import dotenv
import os
import json
import time

dotenv.load_dotenv()

mail = os.getenv("MAIL")
password = os.getenv("PASSWORD")
mail1 = os.getenv("ADRESS_1")
mail2 = os.getenv("ADRESS_2")
zotero_key = os.getenv("ZOTERO_API_KEY")
joplin_key = os.getenv("JOPLIN_API_KEY")


d = requests.get(f"https://api.zotero.org/groups/2611287/items?key={zotero_key}")
print()

with open("../../output_shared.json", "w") as outfile:
    json.dump(d.json(), outfile)

current = []

while True:
    time.sleep(2)
    with open("../../output_shared.json", "r") as file:
        data = json.load(file)
        print(data[0])
