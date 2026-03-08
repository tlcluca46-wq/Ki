import cloudscraper
from bs4 import BeautifulSoup
import json
import datetime

def genera_lista():
    url_sito = "https://www.streameast24.com"
    # Simuliamo un browser mobile per evitare blocchi
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})
    
    canali_finali = []
    
    try:
        print("Recupero dati dal sito...")
        response = scraper.get(url_sito, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cerchiamo i contenitori delle partite (solitamente div o li)
        # Analizzando la struttura tipica di questi siti:
        items = soup.find_all('a', href=True)
        
        for item in items:
            href = item['href']
            # Cerchiamo solo i link ai match
            if "/stream/" in href or "/match/" in href:
                # Pulizia Nome e ricerca Orario
                raw_text = item.get_text(" | ", strip=True)
                # Spesso il testo è: "15:00 | Team A vs Team B"
                
                # Cerchiamo un'immagine nel link o vicino
                img_tag = item.find('img')
                img_url = ""
                if img_tag and img_tag.get('src'):
                    img_url = img_tag['src']
                    if not img_url.startswith('http'):
                        img_url = f"{url_sito}{img_url}"
                else:
                    # Logo di default se non trova l'immagine della partita
                    img_url = "https://www.streameast24.com/favicon.ico"

                full_url = href if href.startswith('http') else f"{url_sito}{href}"
                
                canali_finali.append({
                    "name": raw_text, # Visualizzerà "Orario | Squadre"
                    "url": full_url,
                    "image": img_url,
                    "isHost": True
                })
        
        print(f"Trovati {len(canali_finali)} eventi con loghi.")

    except Exception as e:
        print(f"Errore: {e}")
    
    # Fallback se la lista è vuota
    if not canali_finali:
        canali_finali.append({
            "name": "Nessun evento live ora",
            "url": "https://www.google.com",
            "image": "https://via.placeholder.com/150",
            "isHost": True
        })

    # Struttura JSON finale
    data = {
        "name": "StreamEast Live - Aggiornato",
        "author": "AutoUpdate Mobile",
        "groups": [{
            "name": f"Partite del {datetime.date.today().strftime('%d/%m')}",
            "stations": canali_finali
        }]
    }

    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    genera_lista()
