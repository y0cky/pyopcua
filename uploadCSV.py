from opcua import Client, ua
import pandas as pd

def read_csv(csv_datei):
    """Liest eine CSV-Datei ein und gibt die Daten zurück."""
    try:
        daten = pd.read_csv(csv_datei)
        return daten
    except FileNotFoundError:
        print(f"Die Datei '{csv_datei}' wurde nicht gefunden.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Die Datei '{csv_datei}' ist leer.")
        return None
    except Exception as e:
        print(f"Fehler beim Lesen der CSV-Datei: {e}")
        return None

def write_SPS(client, variable, value_array, value_type):
    """Schreibt einen Wert in eine SPS-Variable."""
    try:
        node_id = f'ns=3;s="Messpunkte_DB"."{variable}"'
        node = client.get_node(node_id)
        
        if value_type == ua.VariantType.Int16:
            value_array = value_array.astype(int)
        
        new_value = ua.DataValue(ua.Variant(value_array.tolist(), value_type))
        node.set_value(new_value)
        print(f"Wert von '{variable}' gesetzt auf: {new_value.Value}")
    except Exception as e:
        print(f"Fehler beim Schreiben in die SPS-Variable '{variable}': {e}")

def read_SPS(client, variable):
    """Liest den Wert einer SPS-Variable."""
    try:
        node_id = f'ns=3;s="Messpunkte_DB"."{variable}"'
        node = client.get_node(node_id)
        current_value = node.get_value()
        print(f"Aktueller Wert von '{variable}': {current_value}")
        return current_value
    except Exception as e:
        print(f"Fehler beim Lesen der SPS-Variable '{variable}': {e}")
        return None

# Die Adresse der OPC-UA-Server-URL
url = "opc.tcp://192.168.0.1:4840"

# Erstelle eine OPC-UA-Client-Instanz
client = Client(url)

try:
    # Verbinde dich mit dem OPC-UA-Server
    client.connect()
    print("Mit OPC-UA-Server verbunden\n")

    print("SPS Auslesen:")
    read_SPS(client, "index")
    read_SPS(client, "drehmoment")
    read_SPS(client, "drehzahl")
    print("SPS auslesen beendet\n")
    
    # CSV Auslesen und Spalten in Array speichern
    daten = read_csv('daten.csv')
    if daten is not None:
        print("SPS schreiben:")
        # Array aus CSV erzeugen und in SPS übertragen
        index_array = daten['index'].values
        print('CSV Index:', index_array)
        write_SPS(client, "index", index_array, ua.VariantType.Int16)
        
        drehzahl_array = daten['drehzahl'].values
        print('CSV Drehzahl:', drehzahl_array)
        write_SPS(client, "drehzahl", drehzahl_array, ua.VariantType.Float)
        
        drehmoment_array = daten['drehmoment'].values
        print('CSV Drehmoment:', drehmoment_array)
        write_SPS(client, "drehmoment", drehmoment_array, ua.VariantType.Float)
        print("SPS schreiben beendet\n")
    else:
        print("SPS-Schreiben wurde übersprungen, da CSV-Daten nicht verfügbar sind.")

except Exception as e:
    print(f"Fehler während der OPC-UA-Kommunikation: {e}")

finally:
    # Trenne die Verbindung zum OPC-UA-Server
    try:
        client.disconnect()
        print("Verbindung zum OPC-UA-Server getrennt")
    except Exception as e:
        print(f"Fehler beim Trennen der Verbindung: {e}")
