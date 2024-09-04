Prüfstand-Management-System für Elektrische Maschinen

Dieses Repository enthält drei Programme zur Verwaltung und Auswertung von Arbeitspunkten auf einem Prüfstand für das Ausmessen elektrischer Maschinen. Die Programme stehen als ausführbare .exe-Dateien im Abschnitt Releases zur Verfügung.
Programme

    Arbeitspunktgenerator: Erstellt Listen von Arbeitspunkten für das Anfahren und Testen des Kennfelds einer elektrischen Maschine im Prüfstandbetrieb.

    UploadCSV: Lädt die Arbeitspunkt-Listen in die Speicherprogrammierbare Steuerung (SPS) des Prüfstands hoch.

    ReadOPCUA: Liest Messergebnisse von der SPS über das OPC UA (Open Platform Communications Unified Architecture) Protokoll aus.

Installation

Die Programme sind als ausführbare .exe-Dateien verfügbar. Du kannst die Installationsdateien aus dem Releases Abschnitt herunterladen.

    Arbeitspunktgenerator
        Gehe zu Releases.
        Lade die .exe-Datei für den Arbeitspunktgenerator herunter.
        Führe die heruntergeladene Datei aus und folge den Installationsanweisungen.

    UploadCSV
        Gehe zu Releases.
        Lade die .exe-Datei für UploadCSV herunter.
        Führe die heruntergeladene Datei aus und folge den Installationsanweisungen.

    ReadOPCUA
        Gehe zu Releases.
        Lade die .exe-Datei für ReadOPCUA herunter.
        Führe die heruntergeladene Datei aus und folge den Installationsanweisungen.

Verwendung
Arbeitspunktgenerator

    Starte das Programm nach der Installation.
    Erstelle eine CSV-Datei mit Arbeitspunkten für das Testen und Kalibrieren der elektrischen Maschine. Das Programm bietet Optionen zur Anpassung der Punktelisten entsprechend den Testanforderungen.

UploadCSV

    Starte das Programm nach der Installation.
    Lade die zuvor erstellten CSV-Dateien in die SPS des Prüfstands hoch. Stelle sicher, dass die Verbindung zur SPS korrekt konfiguriert ist, um die Daten erfolgreich zu übertragen.

ReadOPCUA

    Starte das Programm nach der Installation.
    Lies die Messergebnisse von der SPS aus. Das Programm kommuniziert über das OPC UA Protokoll, daher ist ein entsprechender OPC UA Server erforderlich. Die Ergebnisse werden ausgelesen und stehen zur weiteren Analyse zur Verfügung.

Abhängigkeiten

    Die Programme sind als .exe-Dateien bereitgestellt und enthalten alle notwendigen Abhängigkeiten.
