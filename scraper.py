import cloudscraper
from bs4 import BeautifulSoup
import json
import sys

def genera_lista():
    # Simuliamo un browser Android per bypassare i blocchi
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'android', 'desktop': False}
    )
    lista_totale = []

    # --- SCANSIONE STREAMEAST ---
    try:
        print("Scansione Streameast in corso...")
        r_st = scraper.get("https://www.streameast24.com", timeout=15)
        soup_st = BeautifulSoup(r_st.text, 'html.parser')
        for a in soup_st.find_all('a', href=True):
            href = a['href']
            if "/stream/" in href or "/match/" in href:
                nome = a.get_text(strip=True)
                if nome:
                    lista_totale.append({
                        "name": f"ST | {nome}",
                        "url": href if href.startswith('http') else f"https://www.streameast24.com{href}",
                        "image": "https://www.streameast24.com/favicon.ico",
                        "isHost": True
                    })
    except Exception as e:
        print(f"Errore Streameast: {e}")

    # --- SCANSIONE THE-TV.APP ---
    try:
        print("Scansione The-TV.app in corso...")
        # Aggiungiamo un referer specifico per questo sito
        headers = {'Referer': 'https://the-tv.app/'}
        r_tv = scraper.get("https://the-tv.app", timeout=15, headers=headers)
        soup_tv = BeautifulSoup(r_tv.text, 'html.parser')
        for a in soup_tv.find_all('a', href=True):
            href = a['href']
            if "/event/" in href or "/tv/" in href:
                testo = a.get_text(" ", strip=True)
                if len(testo) > 3:
                    lista_totale.append({
                        "name": f"TV | {testo}",
                        "url": href if href.startswith('http') else f"https://the-tv.app{href}",
                        "image": "https://the-tv.app/favicon.ico",
                        "isHost": True
                    })
    except Exception as e:
        print(f"Errore The-TV: {e}")

    # --- CREAZIONE FILE JSON ---
    if not lista_totale:
        lista_totale.append({
            "name": "⚠️ Nessun match trovato al momento",
            "url": "https://google.com",
            "isHost": True
        })

    output = {
        "name": "I Miei Sport Live",
        "author": "AutoUpdate",
        "groups": [{"name": "Eventi Live", "stations": lista_totale}]
    }

    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"Finito! Trovati {len(lista_totale)} canali.")

if __name__ == "__main__":
    genera_lista()
