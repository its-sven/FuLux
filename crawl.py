import requests
from bs4 import BeautifulSoup

def get_diesel_prices(url):
    # Anfrage an die Webseite senden
    response = requests.get(url)
    
    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        # HTML-Inhalt der Webseite parsen
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # HTML-Elemente finden, die die Dieselpreise enthalten
        diesel_price_element = soup.find('div', class_='cobalt-article__body')  # Diese Klasse kann sich ändern; prüfen Sie die genaue Struktur der Webseite
        if diesel_price_element:
            prices = diesel_price_element.get_text(strip=True)
            print("Aktuelle Dieselpreise:")
            print(prices)
        else:
            print("Fehler: Dieselpreise konnten nicht gefunden werden.")
    else:
        print(f"Fehler bei der Anfrage: {response.status_code}")

if __name__ == "__main__":
    url = "https://www.aral.de/de_lu/luxembourg/home/kraftstoffe-und-preise/aktuelle-kraftstoffpreise.html"
    get_diesel_prices(url)
