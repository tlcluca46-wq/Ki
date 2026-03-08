import cloudscraper
from bs4 import BeautifulSoup
import json
import time

# Configurazione
BASE_URL = "https://www.streameast24.com"
OUTPUT_FILE = "streameast_wiseplay.json"

def get_streams():
    # Creiamo uno scraper che bypassa le protezioni bot di base
    scraper = cloudscraper.create_scraper()
    
    print(f"Accesso a {BASE_URL}...")
    try:
        response = scraper.get(BASE_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cerchiamo i link alle partite (solitamente sono tag <a> con classi specifiche)
        # Nota: I selettori 'a.btn' o 'div.match' cambiano spesso, vanno verificati
        matches = soup.select('a') # Prendiamo tutti i link per ora
        
        lista_canali = []
        
        for match in matches:
            title = match.get_text(strip=True)
            href = match.get('href')
            
            # Filtriamo solo i link che sembrano partite o stream
            if href and ("/stream/" in href or "watch" in href):
                full_url = href if href.startswith('http') else BASE_URL + href
                
                # Aggiungiamo alla lista per Wiseplay
                lista_canali.append({
                    "name": title if title else "Evento Live",
                    "url": full_url, # Inizialmente mettiamo il link della pagina
                    "image": "https://www.streameast24.com/favicon.ico",
                    "isHost": True # Indica a Wiseplay di provare ad aprire il sito
                })
        
        # Creazione struttura W3U (Wiseplay JSON)
        wiseplay_data = {
            "name": "StreamEast Live",
            "author": "AutoScraper",
            "groups": [
                {
                    "name": "Sports Live",
                    "stations": lista_canali
                }
            ]
        }
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(wiseplay_data, f, indent=4, ensure_ascii=False)
            
        print(f"Fatto! Generati {len(lista_canali)} eventi in {OUTPUT_FILE}")

    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    get_streams()

# Nel blocco finale dello script:
with open("playlist.json", "w", encoding="utf-8") as f:
    json.dump(wiseplay_data, f, indent=4)
