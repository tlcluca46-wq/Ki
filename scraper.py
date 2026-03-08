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
            if "/stream/" in a['href'] or "/match/" in a['href']:
                nome = a.get_text(" ", strip=True)
                if nome:
                    canali.append({
                        "name": f"ST | {nome}",
                        "url": a['href'] if a['href'].startswith('http') else f"https://www.streameast24.com{a['href']}",
                        "image": "https://www.streameast24.com/favicon.ico",
                        "isHost": True
                    })
    except Exception as e: print(f"Errore ST: {e}")
    return canali

def estrai_buffstreams(scraper):
    canali = []
    try:
        # Buffstreams usa spesso questa struttura per i match live
        url = "https://buffstreams.plus/index7"
        res = scraper.get(url, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Cerchiamo i "match-box" o i link che contengono webcast
        items = soup.select('a[href*="/webcast/"], a[href*="/watch/"]')
        
        for item in items:
            href = item['href']
            # Pulizia nome: spesso il testo è diviso in più span (squadra A, orario, squadra B)
            nome = item.get_text(" ", strip=True)
            
            img = item.find('img')
            img_url = img['src'] if img and img.get('src') else "https://buffstreams.plus/favicon.ico"
            
            if not img_url.startswith('http'):
                img_url = f"https://buffstreams.plus{img_url}"

            full_url = href if href.startswith('http') else f"https://buffstreams.plus{href}"
            
            if nome and "/webcast/" in full_url:
                canali.append({
                    "name": f"BS | {nome}",
                    "url": full_url,
                    "image": img_url,
                    "isHost": True
                })
    except Exception as e: print(f"Errore BS: {e}")
    return canali

def genera_lista():
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'desktop': False})
    
    st_list = estrai_streameast(scraper)
    bs_list = estrai_buffstreams(scraper)
    
    data = {
        "name": "Live Sports Hub",
        "author": "Gemini-AI",
        "groups": [
            {"name": "🔴 STREAM EAST", "stations": st_list},
            {"name": "🔵 BUFF STREAMS", "stations": bs_list}
        ]
    }
    
    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Aggiornamento completato. Totale canali: {len(st_list) + len(bs_list)}")

if __name__ == "__main__":
    genera_lista()
