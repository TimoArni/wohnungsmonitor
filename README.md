# Wohnungsmonitor

Überwacht regelmäßig die Anzahl von verfügbaren Wohnungen auf einer Website und sendet Push-Benachrichtigungen über Prowl, wenn sich die Anzahl der Wohnungen ändert. Die Anzahl wird in einer JSON-Datei gespeichert und zwischen den Überprüfungen aktualisiert.

## Features
- **Automatische Überprüfung**: Alle 5 Minuten (zwischen 06:00 und 20:00 Uhr).
- **Push-Benachrichtigungen**: Benachrichtigung über Prowl bei Änderung der Anzahl.
- **JSON-Datei zur Nachverfolgung**: Speichert die Anzahl der Wohnungen.
- **GitHub Actions Integration**: Automatische Ausführung des Skripts.

## Voraussetzungen
- GitHub Repository mit aktiviertem **GitHub Actions**.
- **Prowl API Key** (über [Prowl](https://www.prowlapp.com/)).
- **Python** und die Bibliotheken `requests` und `beautifulsoup4`.

## Einrichtung

1. **Clone Repository**:
    ```bash
    git clone https://github.com/DEIN-BENUTZERNAME/wohnungsmonitor.git
    cd wohnungsmonitor
    ```

2. **Prowl API Key als GitHub Secret hinzufügen**: 
    Gehe zu **Settings** > **Secrets and variables** > **Actions** und füge einen neuen Secret `PROWL_API_KEY` hinzu.

3. **JSON-Datei erstellen**:
    Erstelle eine Datei `immobilien_count.json` mit folgendem Inhalt:
    ```json
    {
      "count": null
    }
    ```

## Funktionsweise
- Das Skript wird über GitHub Actions automatisch alle 5 Minuten ausgeführt (06:00 bis 20:00 Uhr).
- Es prüft die Anzahl der Wohnungen und speichert diese in der `immobilien_count.json`.
- Änderungen der Anzahl lösen eine Push-Benachrichtigung aus.

## Workflow

Der Cron-Job für GitHub Actions läuft nach folgendem Zeitplan:

```yaml
*/5 6-19 * * *
