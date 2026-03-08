import cloudscraper
from bs4 import BeautifulSoup
import json
import time

def estrai_streameast(scraper):
    canali = []
    try:
        res = scraper.get("https://www.streameast24.com", timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            if any(x in a['href'] for x in ["/stream/", "/match/"]):
                nome = a.get_text(" ", strip=True)
                if nome:
                    canali.append({
                        "name": f"ST | {nome}",
                        "url": a['href'] if a['href'].startswith('http') else f"https://www.streameast24.com{a['href']}",
                        "image": "https://www.streameast24.com/favicon.ico",
                        "isHost": True
                    })
    except Exception as e:
        print(f"Errore Streameast: {e}")
    return canali

def estrai_the_tv(scraper):
    canali = []
    try:
        # Questo sito spesso richiede un 'referer' per mostrare i contenuti
        headers = {'Referer': 'https://the-tv.app/'}
        res = scraper.get("https://the-tv.app/", timeout=15, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Cerchiamo i blocchi che contengono gli eventi
        # Spesso sono link con classi tipo 'channel-card' o dentro liste specifiche
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Filtriamo per i link ai canali o eventi live
            if "/tv/" in href or "/event/" in href:
                # Recuperiamo tutto il testo (che di solito include orario e nome)
                testo = a.get_text(" ", strip=True)
                
                # Pulizia minima del testo
                if testo and len(testo) > 5:
                    full_url = href if href.startswith('http') else f"https://the-tv.app{href}"
                    canali.append({
                        "name": f"TV | {testo
