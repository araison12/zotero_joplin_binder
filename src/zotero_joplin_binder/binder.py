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
    d = requests.get(
        f"https://api.zotero.org/groups/2611287/collections?key={zotero_key}"
    )

    with open("../../data/shared_collections.txt", "w") as output:
        json.dump(d.json(), output)
    i = 0
    for col in d.json():
        l = requests.get(
            f"""https://api.zotero.org/groups/2611287/collections/{col['key']}/items?key={zotero_key}"""
        )
        with open(f"../../data/shared_items_collection_{i}.txt", "w") as output0:
            json.dump(l.json(), output0)
        i += 1
        for item in l.json():
            couple = (col["key"], item["key"])
            if couple in current_items:
                continue
            else:
                current_items.append(couple)
                try:
                    sender = os.getenv("EMAIL")
                    password = os.getenv("PASSWORD")
                    receivers = [mail, mail1, mail2]
                    smtp_serv = os.getenv("SERVER")
                    port = 587
                    from email.message import EmailMessage

                    msg = EmailMessage()
                    content = f"""
                    A new item as been added to our Zotero shared library {item['library']['name']} by
                    {item['meta']['createdByUser']['username']}.
                    The new article is :
                    - Title : {item['data']['title']}

                    - Authors : {[
                    " ".join([it["firstName"], it["lastName"]])
                        for it in item["data"]["creators"]
                        ]}
                        - Date : {item['data']['date']}

                        - URL : {item['data']['url']}
 
                        - Abstract : {item['data']['abstractNote']}
                        """
                    msg[
                        "Subject"
                    ] = f"""New document {item["data"]["title"]} in {item['library']['name']} by {item['meta']['createdByUser']['username']}"""
                    msg["From"] = os.getenv("EMAIL")
                    msg["To"] = ", ".join(receivers)
                    msg.set_content(content)
                    with smtplib.SMTP(smtp_serv, port) as server:
                        server.login(sender, password)
                        server.send_message(msg)
                    # authors = [
                    #     " ".join([it["firstName"], it["lastName"]])
                    #     for it in item["data"]["creators"]
                    # ]
                    # with open("../../data/buffer.txt", "w") as buffer:

                    #     data_json = str(
                    #         {
                    #             "title": str(item["data"]["title"])
                    #             + " -"
                    #             + " ".join(authors),
                    #             "body": f"""
                    #             - Date : {item['data']['date']}
                    #             - URL : {item['data']['url']}
                    #             - Abstract : {item['data']['abstractNote']}
                    #             - Key Words:
                    #             - General subject:
                    #             - Specific subject:
                    #             - Hypothesis:
                    #             - Methodology:
                    #             - Result(s):
                    #             - Summary of key points:
                    #             - Context (how this article relates to other work in the field; how it ties in with key issues
                    #              and findings by others, including yourself):
                    #             - Significance (to the field; in relation to your own work):
                    #             - Important Figures and/or Tables (brief description; page number):
                    #             - Cited References to follow up on (cite those obviously related to your topic AND any
                    #              papers frequently cited by others because those works may well prove to be essential as
                    #              you develop your own work):
                    #             - Your comments on the work:
                    #             - How this reading relates to others you have read:
                    #             """,
                    #         }
                    #     )
                    #     buffer.write(data_json)
                    # os.system(
                    #     f"""curl http://localhost:41184/notes?token={joplin_key} -d @../../data/buffer.txt"""
                    # )
                except KeyError:
                    continue
