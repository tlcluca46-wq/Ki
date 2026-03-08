import cloudscraper
from bs4 import BeautifulSoup
import json
import datetime

def estrai_dati(url, scraper, selettore_link):
    canali = []
    try:
        response = scraper.get(url, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            # Filtro per link di streaming
            if any(x in href for x in ["/stream/", "/match/", "/live/"]):
                full_url = href if href.startswith('http') else f"{url.split('.plus')[0]}.plus{href}"
                
                # Cerchiamo il testo e l'immagine
                nome = link.get_text(" ", strip=True)
                img = link.find('img')
                img_url = img['src'] if img and img.get('src') else "https://buffstreams.plus/favicon.ico"
                if img_url and not img_url.startswith('http'):
                    img_url = f"https://buffstreams.plus{img_url}"

                canali.append({
                    "name": nome if nome else "Evento Live",
                    "url": full_url,
                    "image": img_url,
                    "isHost": True
                })
        return canali
    except Exception as e:
        print(f"Errore su {url}: {e}")
        return []

def genera_lista_multisito():
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})
    
    # Estrazione dai due siti
    canali_streameast = estrai_dati("https://www.streameast24.com", scraper, "/stream/")
    canali_buff = estrai_dati("https://buffstreams.plus/index7", scraper, "/webcast/")

    # Creazione struttura Wiseplay con GRUPPI
    data = {
        "name": "I Miei Sport Live",
        "author": "AutoUpdate",
        "groups": [
            {
                "name": "🔴 STREAM EAST",
                "stations": canali_streameast
            },
            {
                "name": "🔵 BUFF STREAMS",
                "stations": canali_buff
            }
        ]
    }

    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Playlist aggiornata con successo!")

if __name__ == "__main__":
    genera_lista_multisito()
