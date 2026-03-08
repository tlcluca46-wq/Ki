import cloudscraper
from bs4 import BeautifulSoup
import json
import datetime

def estrai_dati(url, scraper, parole_chiave):
    canali = []
    try:
        print(f"Analizzando: {url}")
        response = scraper.get(url, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cerchiamo tutti i link
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            testo = link.get_text(" ", strip=True)
            
            # Filtro: il link deve contenere una delle parole chiave (es. 'webcast' o 'stream')
            if any(key in href.lower() for key in parole_chiave):
                # Gestione URL relativi
                if href.startswith('/'):
                    # Estraiamo il dominio base (es. https://buffstreams.plus)
                    base = "/".join(url.split("/")[:3])
                    full_url = f"{base}{href}"
                else:
                    full_url = href
                
                # Cerchiamo l'immagine
                img = link.find('img')
                img_url = img['src'] if img and img.get('src') else ""
                if img_url and img_url.startswith('/'):
                    base = "/".join(url.split("/")[:3])
                    img_url = f"{base}{img_url}"

                # Evitiamo duplicati o link vuoti
                if testo and full_url not in [c['url'] for c in canali]:
                    canali.append({
                        "name": testo,
                        "url": full_url,
                        "image": img_url if img_url else "https://buffstreams.plus/favicon.ico",
                        "isHost": True
                    })
        return canali
    except Exception as e:
        print(f"Errore su {url}: {e}")
        return []

def genera_lista_multisito():
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})
    
    # Parole chiave specifiche per Buffstreams: spesso usano 'webcast' o 'watch'
    canali_streameast = estrai_dati("https://www.streameast24.com", scraper, ["/stream/", "/match/"])
    canali_buff = estrai_dati("https://buffstreams.plus/index7", scraper, ["/webcast/", "/watch/", "buffstreams.plus/"])

    data = {
        "name": "Super Lista Sport",
        "author": "AutoUpdate",
        "groups": [
            {"name": "🔴 STREAM EAST", "stations": canali_streameast},
            {"name": "🔵 BUFF STREAMS", "stations": canali_buff}
        ]
    }

    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Completato! Streameast: {len(canali_streameast)} | Buff: {len(canali_buff)}")

if __name__ == "__main__":
    genera_lista_multisito()
