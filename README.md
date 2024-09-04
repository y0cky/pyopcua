# Prüfstand-Management-System für Elektrische Maschinen

Dieses Repository enthält drei Programme zur Verwaltung und Auswertung von Arbeitspunkten auf einem Prüfstand für das Ausmessen elektrischer Maschinen. Die Programme stehen als ausführbare `.exe`-Dateien im Abschnitt [Releases](https://github.com/y0cky/pyopcua/releases) zur Verfügung.

## Programme

1. **Arbeitspunktgenerator**: Erstellt Listen von Arbeitspunkten für das Anfahren und Testen des Kennfelds einer elektrischen Maschine im Prüfstandbetrieb.

2. **UploadCSV**: Lädt die Arbeitspunkt-Listen in die Speicherprogrammierbare Steuerung (SPS) des Prüfstands hoch.

3. **ReadOPCUA**: Liest Messergebnisse von der SPS über das OPC UA (Open Platform Communications Unified Architecture) Protokoll aus.

## Installation

Die Programme sind als ausführbare `.exe`-Dateien verfügbar. Folge diesen Schritten, um die Programme zu installieren:

### 1. Arbeitspunktgenerator

- Gehe zu [Releases](https://github.com/y0cky/pyopcua/releases).
- Lade die `.exe`-Datei für den Arbeitspunktgenerator herunter.
- Führe die heruntergeladene Datei aus und folge den Installationsanweisungen.

### 2. UploadCSV

- Gehe zu [Releases](https://github.com/y0cky/pyopcua/releases).
- Lade die `.exe`-Datei für UploadCSV herunter.
- Führe die heruntergeladene Datei aus und folge den Installationsanweisungen.

### 3. ReadOPCUA

- Gehe zu [Releases](https://github.com/y0cky/pyopcua/releases).
- Lade die `.exe`-Datei für ReadOPCUA herunter.
- Führe die heruntergeladene Datei aus und folge den Installationsanweisungen.

## Verwendung

### Arbeitspunktgenerator

- Starte das Programm nach der Installation.
- Erstelle eine CSV-Datei mit Arbeitspunkten für das Testen und Kalibrieren der elektrischen Maschine. Das Programm bietet Optionen zur Anpassung der Punktelisten entsprechend den Testanforderungen.

### UploadCSV

- Starte das Programm nach der Installation.
- Lade die zuvor erstellten CSV-Dateien in die SPS des Prüfstands hoch. Vergewissere dich, dass die Verbindung zur SPS korrekt konfiguriert ist, um die Daten erfolgreich zu übertragen.

### ReadOPCUA

- Starte das Programm nach der Installation.
- Lies die Messergebnisse von der SPS aus. Das Programm kommuniziert über das OPC UA Protokoll, daher ist ein entsprechender OPC UA Server erforderlich. Die Ergebnisse werden ausgelesen und stehen zur weiteren Analyse bereit.

## Abhängigkeiten

- Die Programme sind als `.exe`-Dateien bereitgestellt und enthalten alle notwendigen Abhängigkeiten.

