import requests
import re
import os

# URL der Website
URL = 'https://www.saga.hamburg/immobiliensuche?Kategorie=APARTMENT'

# Prowl API-Schlüssel (aus der E-Mail-Adresse extrahiert)
API_KEY = os.environ.get('PROWL_API_KEY')
PROWL_URL = 'https://api.prowlapp.com/publicapi/add'

# Datei zum Speichern der vorherigen Anzahl
COUNT_FILE = 'previous_count.txt'

def fetch_current_count():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        content = response.text

        # Regex, um die Anzahl der Ergebnisse zu finden
        match = re.search(r'(\d+)\s*Ergebnisse', content)
        if match:
            current_count = int(match.group(1))
            print(f'Aktuelle Anzahl der Wohnungen: {current_count}')
            return current_count
        else:
            print("Konnte die Anzahl der Ergebnisse nicht finden.")
            return None
    except Exception as e:
        print(f'Fehler beim Abrufen der Website: {e}')
        return None

def read_previous_count():
    if os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'r') as f:
            try:
                return int(f.read())
            except ValueError:
                return None
    else:
        return None  # Datei existiert nicht

def write_current_count(count):
    with open(COUNT_FILE, 'w') as f:
        f.write(str(count))
    print(f'Datei {COUNT_FILE} wurde aktualisiert.')

def send_prowl_notification(event, description):
    data = {
        'apikey': API_KEY,
        'application': 'Wohnungsmonitor',
        'event': event,
        'description': description,
    }
    try:
        response = requests.post(PROWL_URL, data=data)
        if response.status_code == 200:
            print('Benachrichtigung gesendet.')
        else:
            print(f'Fehler beim Senden der Benachrichtigung: {response.text}')
    except Exception as e:
        print(f'Fehler bei der Kommunikation mit Prowl: {e}')

def main():
    current_count = fetch_current_count()
    if current_count is None:
        return

    previous_count = read_previous_count()
    if previous_count is None:
        # Erste Ausführung, speichere die aktuelle Anzahl
        write_current_count(current_count)
        print('Erste Ausführung, vorherige Anzahl nicht vorhanden.')
        return

    if current_count != previous_count:
        if current_count > previous_count:
            event = 'Neue Wohnung verfügbar'
            description = f'Es gibt jetzt {current_count} Wohnungen (vorher {previous_count}).'
        else:
            event = 'Weniger Wohnungen verfügbar'
            description = f'Es gibt jetzt {current_count} Wohnungen (vorher {previous_count}).'

        send_prowl_notification(event, description)
        write_current_count(current_count)
    else:
        print('Keine Änderung in der Anzahl der Wohnungen.')

if __name__ == "__main__":
    main()
