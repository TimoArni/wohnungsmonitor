import requests
from bs4 import BeautifulSoup
import re
import json
import os  # Umgebungsvariablen nutzen

# Prowl API Key aus Umgebungsvariablen laden
API_KEY = os.getenv("PROWL_API_KEY")

# URL der Webseite
url = "https://www.saga.hamburg/immobiliensuche?Kategorie=APARTMENT"

# User-Agent simuliert einen Browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# Funktion zum Versenden der Push-Nachricht
def send_push_notification(message):
    prowl_url = f"https://api.prowlapp.com/publicapi/add?apikey={API_KEY}&application=Immobilien&event=Anzahl%20Verändert&description={message}"
    response = requests.get(prowl_url)
    
    # Test-Output, um sicherzustellen, dass der Request gesendet wurde
    if response.status_code == 200:
        print("Push-Nachricht erfolgreich gesendet!")
    else:
        print(f"Fehler beim Senden der Push-Nachricht: {response.status_code}")

# Funktion, um die Anzahl der Ergebnisse zu extrahieren
def get_immobilien_count():
    response = requests.get(url, headers=headers)
    
    # Ausgabe des gesamten Inhalts der Webseite
    print(response.text)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Suche nach dem Text "Ergebnisse" und extrahiere die Zahl davor
    text = soup.get_text()
    match = re.search(r'(\d+)\s+Ergebnisse', text)

    if match:
        return int(match.group(1))
    return None

# Vergleich mit vorheriger Anzahl
def check_for_changes(test_mode=False):
    try:
        with open("immobilien_count.json", "r") as f:
            last_count = json.load(f).get("count")
    except FileNotFoundError:
        last_count = None

    current_count = get_immobilien_count()

    if current_count is not None:
        if test_mode or last_count is None or current_count != last_count:
            message = f"Die Anzahl der verfügbaren Wohnungen hat sich geändert: {current_count} Ergebnisse."
            send_push_notification(message)
            with open("immobilien_count.json", "w") as f:
                json.dump({"count": current_count}, f)
        else:
            print(f"Keine Änderung der Ergebnisse: {current_count} Ergebnisse.")
    else:
        print("Fehler beim Abrufen der Immobilienanzahl.")

# Testmodus aktivieren, um sicherzustellen, dass die Push-Benachrichtigung ausgelöst wird
check_for_changes(test_mode=True)
