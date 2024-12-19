"""
Hae postit rajapinnasta https://jsonplaceholder.typicode.com/posts
Sieltä tulee lista posteja, joista laske jokaiselle käyttäjälle
postien lukumäärä,
Summa: sanojen määrä yhteensä (body)
Keskiarvo: sanojen määrä keskimäärin per postaus
Lisäksi vielä kiinnostaa mitkä ovat top 5 eniten toistuvaa sanaa posteissa (body)
Tallenna nämä tiedot json-tiedostoon, sopivaan tietomalliin. 
Pohdi siis, miten saat tietoja laskettua, ja minkälaiseen rakenteeseen ne olisi hyvä tallentaa, että niitä voi helposti hyödyntää, vaikka toisessa sovelluksessa.
"""

import json
import requests as r

def main():
    URL : str = "https://jsonplaceholder.typicode.com/posts"
    users : dict = {}

    # haetaan postit rajapinnasta ja muutetaan json muotoon
    data = json.loads(r.get(URL).text)
    
    for i in data:
        id = i["userId"]
        body = i["body"]

        if id not in users:
            users.update(add_user(id))

        users[id]["postien_lkm"] += 1
        users[id]["sanojen_yht_lkm"] += word_count(body)
        users[id]["sanojen_keskiarvo"] = users[id]["sanojen_yht_lkm"] / users[id]["postien_lkm"]

        for sana in clean_text(body).split(" "): 
            if sana in users[id]["top_5_sanat"]:
                users[id]["top_5_sanat"][sana] += 1
            else:
                users[id]["top_5_sanat"].update({sana : 1})
                
    # sorttaa top 5 sanat
    for id in users:
        users[id]["top_5_sanat"] = dict(sorted(users[id]["top_5_sanat"].items(), key = lambda item : item[1], reverse = True)[:5])
    
    save_dict(users)
 
def save_dict(dict : dict):
    """
    tallentaa tiedot json-muodossa
    """
    with open("users.json", "w") as f:
        json.dump(dict, f, indent = 4)


def clean_text(text : str) -> str:
    """
    siistii tekstin välinvaihdosta
    """
    return text.replace("\n", " ")


## palauttaa sanojen lukumäärän
def word_count(text : str) -> int:
    """
    palauttaa sanojen lukumäärän
    """
    return len(clean_text(text).split(" "))


## tekee uuden käytäjän tiedot
def add_user(id : int) -> dict:
    """
    tekee uuden käyttäjän tiedot
    """

    return {
        id : {
            "postien_lkm" : 0,
            "sanojen_yht_lkm" : 0,
            "sanojen_keskiarvo" : 0,
            "top_5_sanat" : {}
        }
    }


if __name__ == "__main__":
    main()