import cloudscraper
from bs4 import BeautifulSoup
import json
import datetime

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
    except: pass
    return canali

def estrai_the_tv(scraper):
    canali = []
    try:
        url_base = "https://the-tv.app"
        res = scraper.get(url_base, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # In the-tv.app gli eventi sono spesso in card o liste con orari
        # Cerchiamo i link che portano ai canali o eventi
        for item in soup.find_all(['a', 'div'], class_=True):
            # Questa parte cerca di identificare i blocchi evento (classi comuni: 'event', 'channel')
            link = item if item.name == 'a' else item.find('a', href=True)
            if link and link.get('href'):
                href = link['href']
                # Prendiamo solo link pertinenti
                if "/tv/" in href or "/event/" in href:
                    testo = item.get_text(" ", strip=True)
                    # Spesso l'orario è contenuto nel testo o in uno span specifico
                    # Esempio: "20:45 Milan
