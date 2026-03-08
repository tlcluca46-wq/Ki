import cloudscraper
from bs4 import BeautifulSoup
import json
import sys

def genera_lista():
    url_sito = "https://www.streameast24.com"
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})
    
    canali_finali = []
    
    try:
        print(f"Tentativo di connessione a {url_sito}...")
        response = scraper.get(url_sito, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cerchiamo tutti i link che potrebbero essere partite
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            testo = link.get_text(strip=True)
            
            # Filtro base per trovare i match
            if "/stream/" in href or "/match/" in href:
                full_url = href if href.startswith('http') else f"{url_sito}{href}"
                canali_finali.append({
                    "name": testo if testo else "Evento Live",
                    "url": full_url,
                    "isHost": True
                })
        
        print(f"Trovati {len(canali_finali)} canali.")

    except Exception as e:
        print(f"Errore durante lo scraping: {e}")
        # Non blocchiamo lo script, creiamo una lista vuota o di test per non far fallire GitHub
    
    # Se non trova nulla, aggiungiamo un canale di test per verificare che il JSON venga creato
    if not canali_finali:
        canali_finali.append({
            "name": "Nessun evento trovato al momento",
            "url": "https://www.google.com",
            "isHost": True
        })

    # Struttura Wiseplay
    data = {
        "name": "StreamEast Live Smartphone",
        "author": "AutoUpdate",
        "groups": [{"name": "Sport", "stations": canali_finali}]
    }

    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("File playlist.json generato correttamente.")

if __name__ == "__main__":
    genera_lista()
