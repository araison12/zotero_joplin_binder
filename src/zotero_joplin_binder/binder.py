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


current_items = []

while True:
    time.sleep(2)
    with open("../../output_shared.json", "r") as file:
        d = requests.get(
            f"https://api.zotero.org/groups/2611287/collections?key={zotero_key}"
        )
        for col in d.json():
            l = requests.get(
                f"""https://api.zotero.org/groups/2611287/collections/{col['key']}/items?key={zotero_key}"""
            )
            for item in l.json():

                couple = (col["key"], item["key"])
                if couple in current_items:
                    continue
                else:
                    current_items.append(couple)
                    try:
                        sender = os.getenv("EMAIL")
                        password = os.getenv("PASSWORD")
                        receivers = ["adrienrsn@gmail.com"]
                        smtp_serv = os.getenv("SERVER")
                        port = 587
                        from email.message import EmailMessage

                        msg = EmailMessage()
                        content = f"""
                        "Authors : {[
                                " ".join([it["firstName"], it["lastName"]])
                                for it in item["data"]["creators"]
                            ]}
                        Title : {item["data"]["title"]}
                        Url : {item["data"]["url"]}
                        """

                        msg[
                            "Subject"
                        ] = f"""A new document {item["data"]["title"]} has been added to our shared library"""
                        msg["From"] = os.getenv("EMAIL")
                        msg["To"] = ", ".join(receivers)
                        msg.set_content(content)

                        with smtplib.SMTP(smtp_serv, port) as server:
                            server.login(sender, password)
                            server.send_message(msg)
                    except KeyError:
                        continue
