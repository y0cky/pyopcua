from opcua import Client
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import csv
from datetime import datetime

# URL des OPC UA Servers
url = "opc.tcp://192.168.0.1:4840"

# GUI Setup
root = tk.Tk()
root.title("OPC UA Daten")

# Frame für Treeview und Scrollbars
frame = tk.Frame(root)
frame.pack(expand=True, fill='both')

# Erstelle eine Tabelle (Treeview) mit zusätzlichen Spalten
columns = ["SeqNo", "Datum/Uhrzeit", "Drehzahl", "Drehmoment", "Mechanische Leistung", "Strom", "Spannung", "Elektrische Leistung", "eta", "Temperatur", "DC Strom", "DC Spannung"]
tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)

# Definiere die Spaltenüberschriften
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

# Erstelle Scrollbars
vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

# Packe Treeview und Scrollbars
tree.grid(row=0, column=0, sticky='nsew')
vsb.grid(row=0, column=1, sticky='ns')
hsb.grid(row=1, column=0, sticky='ew')

# Konfiguriere das Grid-System
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Steuerung für Datenlogging
logging = False
data_log = []
seq_no = 0  # Sequenznummer initialisieren

def start_logging():
    global logging, data_log, seq_no
    logging = True
    data_log = []  # Leere die Protokollliste
    seq_no = 0  # Setze die Sequenznummer zurück
    log_button.config(text="Stop Logging")
    tree.delete(*tree.get_children())  # Lösche alle Einträge in der Tabelle
    print("Data logging started")

def stop_logging():
    global logging
    logging = False
    log_button.config(text="Start Logging")
    print("Data logging stopped")
    save_to_csv()

def save_to_csv():
    if not data_log:
        messagebox.showinfo("Info", "No data to save.")
        return
    
    # Standard-Dateiname basierend auf Datum und Uhrzeit
    default_filename = datetime.now().strftime("opcua_data_log_%Y%m%d_%H%M%S.csv")
    
    # Dateiauswahl-Dialog zum Speichern der CSV-Datei
    filename = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=default_filename, filetypes=[("CSV files", "*.csv"), ("All files", "*.*")], title="Save CSV file")
    if not filename:
        return  # Benutzer hat den Dialog abgebrochen

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Header row
        writer.writerows(data_log)  # Data rows
    messagebox.showinfo("Info", f"Data saved to {filename}")
    print(f"Data saved to {filename}")

# Button zum Starten und Stoppen des Datenloggings
log_button = tk.Button(root, text="Start Logging", command=lambda: start_logging() if not logging else stop_logging())
log_button.pack(pady=10)

# Verbindung zum OPC UA Server herstellen
client = Client(url)
previous_data_values = None  # Initialisiere die globale Variable

try:
    client.connect()
    print("Connected to OPC-UA server\n")

    # Funktion zum Auslesen der Daten
    def read_data_array():
        # Lese die Daten aus dem OPC UA-Server
        data_nodes = {
            "Drehzahl": 'ns=3;s="DataLogging_DB"."Data"."n"',
            "Drehmoment": 'ns=3;s="DataLogging_DB"."Data"."M"',
            "Mechanische Leistung": 'ns=3;s="DataLogging_DB"."Data"."Pmech"',
            "Strom": 'ns=3;s="DataLogging_DB"."Data"."I"',
            "Spannung": 'ns=3;s="DataLogging_DB"."Data"."U"',
            "Elektrische Leistung": 'ns=3;s="DataLogging_DB"."Data"."Pauf"',
            "eta": 'ns=3;s="DataLogging_DB"."Data"."eta"',
            "Temperatur": 'ns=3;s="DataLogging_DB"."Data"."Temperatur"',
            "DC Strom": 'ns=3;s="DataLogging_DB"."Data"."I_R_mess"',
            "DC Spannung": 'ns=3;s="DataLogging_DB"."Data"."U_R_mess"'
        }
        data = []
        for key in columns[2:]:  # Die Daten beginnen ab der 3. Spalte
            node_id = data_nodes[key]
            data_node = client.get_node(node_id)
            value = data_node.get_value()
            data.append(value)
        return data

    # Update GUI mit den neuen Daten
    def update_gui():
        global previous_data_values, data_log, seq_no
        current_data_values = read_data_array()

        # Überprüfen, ob sich die Werte geändert haben
        if previous_data_values is None or current_data_values != previous_data_values:
            print("Datenänderung erkannt!")
            
            # 0.1 Sekunden warten, um sicherzustellen, dass alle Daten richtig sind
            root.after(100, process_data, current_data_values)
        
        # Wiederhole die Überprüfung nach einer Sekunde
        root.after(1000, update_gui)

    def process_data(current_data_values):
        global previous_data_values, data_log, seq_no
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_data = [seq_no, timestamp] + current_data_values
        tree.insert("", "end", values=row_data)

        # Daten zur Protokolldatei hinzufügen, falls Logging aktiviert ist
        if logging:
            data_log.append(row_data)
            seq_no += 1  # Erhöhe die Sequenznummer
        
        # Update die vorherigen Werte
        previous_data_values = current_data_values

    # Starte die GUI
    update_gui()
    root.mainloop()

finally:
    # Verbindung trennen
    client.disconnect()
    print("Disconnected from OPC-UA server")
