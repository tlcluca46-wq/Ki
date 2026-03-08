import cloudscraper
from bs4 import BeautifulSoup
import json

def estrai(url, nome_prefisso, scraper):
    canali = []
    try:
        # Usiamo un timeout più lungo e un header più realistico
        res = scraper.get(url, timeout=20)
        if res.status_code != 200:
            print(f"Errore {res.status_code} su {url}")
            return []
            
        soup = BeautifulSoup(res.text, 'html.parser')
        # Cerchiamo TUTTI i link che portano a partite (filtro largo)
        for a in soup.find_all('a', href=True):
            href = a['href']
            testo = a.get_text(" ", strip=True)
            
            # Cattura link con parole chiave comuni nello streaming
            if any(x in href.lower() for x in ['/stream', '/match', '/webcast', '/live', '/watch']):
                full_url = href if href.startswith('http') else f"{url.rstrip('/')}/{href.lstrip('/')}"
                if len(testo) > 3: # Evita link vuoti
                    canali.append({
                        "name": f"{nome_prefisso} | {testo}",
                        "url": full_url,
                        "image": "https://via.placeholder.com/150", # Logo temporaneo
                        "isHost": True
                    })
        return canali
    except Exception as e:
        print(f"Errore critico su {url}: {e}")
        return []

def genera():
    # Creiamo uno scraper che simula perfettamente un browser mobile
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'android',
            'desktop': False
        }
    )
    
    st = estrai("https://www.streameast24.com", "ST", scraper)
    bs = estrai("https://buffstreams.plus/index7", "BS", scraper)
    
    # Se entrambi falliscono, mettiamo un segnale di debug
    if not st and not bs:
        risultato = [{"name": "⚠️ Siti bloccati o nessuna partita ora", "url": "https://google.com"}]
    else:
        risultato = st + bs

    data = {
        "name": "Lista Sport Live",
        "groups": [{"name": "Eventi", "stations": risultato}]
    }
    
    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    genera()
