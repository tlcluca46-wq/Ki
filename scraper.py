import json

# Questa è la struttura base. Qui puoi aggiungere o modificare i link.
# In futuro, potremo automatizzare il "recupero" dei link con lo script di prima.
canali = [
    {
        "name": "StreamEast Live 1",
        "url": "https://www.streameast24.com/", # URL del sito o link diretto se lo hai
        "image": "https://www.streameast24.com/favicon.ico",
        "isHost": True 
    },
    {
        "name": "Esempio Canale Diretto",
        "url": "http://esempio.com/flusso.m3u8",
        "image": "https://via.placeholder.com/150"
    }
]

wiseplay_list = {
    "name": "La Mia Lista Sport",
    "author": "MioAccount",
    "groups": [
        {
            "name": "Calcio & Sport",
            "stations": canali
        }
    ]
}

with open("lista_condivisa.json", "w", encoding="utf-8") as f:
    json.dump(wiseplay_list, f, indent=4, ensure_ascii=False)

print("File lista_condivisa.json creato correttamente!")
