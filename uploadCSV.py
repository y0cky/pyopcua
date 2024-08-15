import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel
import pandas as pd
import numpy as np
from opcua import Client, ua

# Globale Variablen für Einstellungen
opcua_url = "opc.tcp://192.168.0.1:4840"
db_name = "Messpunkte_DB"
namespace_index = 3
opcua_username = ""
opcua_password = ""

# Globale Variable für Daten
daten = None

# CSV Datei öffnen
def read_csv(csv_datei):
    try:
        daten = pd.read_csv(csv_datei)
        return daten
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Lesen der CSV-Datei: {e}")
        return None

# Variable in SPS schreiben
def write_SPS(variable, value_array, value_type):
    try:
        node_id = f'ns={namespace_index};s="{db_name}"."{variable}"'
        node = client.get_node(node_id)
        
        if value_type == ua.VariantType.Int16:
            value_array = value_array.astype(int)
        
        new_value = ua.DataValue(ua.Variant(value_array.tolist(), value_type))
        node.set_value(new_value)
        print(f"Value of '{variable}' set to: {new_value.Value}")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Schreiben der Variable in SPS: {e}")

# Variable in SPS lesen
def read_SPS(variable):
    try:
        node_id = f'ns={namespace_index};s="{db_name}"."{variable}"'
        node = client.get_node(node_id)
        current_value = node.get_value()
        print(f"Current value of '{variable}': {current_value}")
        return current_value
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Lesen der Variable aus SPS: {e}")
        return None

# Verbindung zu OPC-UA Server herstellen
def connect_to_server():
    global client
    try:
        client = Client(opcua_url)
        if opcua_username and opcua_password:
            client.set_user(opcua_username)
            client.set_password(opcua_password)
        client.connect()
        btn_connect.config(bg="green")  # Button in Grün ändern
        print("Connected to OPC-UA server")
        messagebox.showinfo("Erfolg", "Erfolgreich mit OPC-UA Server verbunden")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Verbinden zum OPC-UA Server: {e}")

# Verbindung zu OPC-UA Server trennen
def disconnect_from_server():
    try:
        client.disconnect()
        btn_connect.config(bg="SystemButtonFace")  # Button zurücksetzen
        print("Disconnected from OPC-UA server")
        messagebox.showinfo("Erfolg", "Verbindung zum OPC-UA Server getrennt")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Trennen vom OPC-UA Server: {e}")

# CSV Datei hochladen und anzeigen
def upload_csv():
    global daten
    csv_datei = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if csv_datei:
        daten = read_csv(csv_datei)
        if daten is not None:
            messagebox.showinfo("Erfolg", "CSV Datei erfolgreich hochgeladen")
            # Anzeigen der vollständigen Daten der CSV-Datei
            display_data(daten)

# CSV-Daten in der GUI anzeigen
def display_data(daten):
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, "\n\n--- Full Data ---\n\n")
    text_widget.insert(tk.END, daten.to_string())

# Daten an SPS senden
def send_to_sps():
    global daten
    if daten is None:
        messagebox.showerror("Fehler", "Keine CSV-Daten zum Senden. Bitte laden Sie zuerst eine CSV-Datei hoch.")
        return

    try:
        index_array = np.zeros(1000, dtype=np.int16)
        drehzahl_array = np.zeros(1000, dtype=np.float32)
        drehmoment_array = np.zeros(1000, dtype=np.float32)

        rows_to_copy = min(len(daten), 1000)
        index_array[:rows_to_copy] = daten['index'][:rows_to_copy].values
        drehzahl_array[:rows_to_copy] = daten['drehzahl'][:rows_to_copy].values
        drehmoment_array[:rows_to_copy] = daten['drehmoment'][:rows_to_copy].values
        
        write_SPS("index", index_array, ua.VariantType.Int16)
        write_SPS("drehzahl", drehzahl_array, ua.VariantType.Float)
        write_SPS("drehmoment", drehmoment_array, ua.VariantType.Float)
        
        messagebox.showinfo("Erfolg", "Daten erfolgreich an SPS gesendet")
    except KeyError as e:
        messagebox.showerror("Fehler", f"Fehlender Spaltenname in der CSV-Datei: {e}")

# Daten manuell eingeben
def enter_data_manually():
    def on_submit():
        try:
            start_drehzahl = float(entry_start_drehzahl.get())
            step_drehzahl = float(entry_step_drehzahl.get())
            end_drehzahl = float(entry_end_drehzahl.get())
            
            start_drehmoment = float(entry_start_drehmoment.get())
            step_drehmoment = float(entry_step_drehmoment.get())
            end_drehmoment = float(entry_end_drehmoment.get())
            
            drehzahl_values = np.arange(start_drehzahl, end_drehzahl + step_drehzahl, step_drehzahl)
            drehmoment_values = np.arange(start_drehmoment, end_drehmoment + step_drehmoment, step_drehmoment)
            
            data = [(i, dz, dm) for i, (dz, dm) in enumerate(np.array(np.meshgrid(drehzahl_values, drehmoment_values)).T.reshape(-1, 2))]
            
            global daten
            daten = pd.DataFrame(data, columns=['index', 'drehzahl', 'drehmoment'])
            
            display_data(daten)
            manual_entry_window.destroy()
            messagebox.showinfo("Erfolg", "Daten erfolgreich manuell eingegeben")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der manuellen Dateneingabe: {e}")

    # Fenster für die manuelle Eingabe
    manual_entry_window = Toplevel(root)
    manual_entry_window.title("Daten manuell eingeben")

    # Drehzahl Eingabe
    tk.Label(manual_entry_window, text="Anfangswert Drehzahl:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    entry_start_drehzahl = tk.Entry(manual_entry_window)
    entry_start_drehzahl.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(manual_entry_window, text="Schrittweite Drehzahl:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    entry_step_drehzahl = tk.Entry(manual_entry_window)
    entry_step_drehzahl.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(manual_entry_window, text="Endwert Drehzahl:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    entry_end_drehzahl = tk.Entry(manual_entry_window)
    entry_end_drehzahl.grid(row=2, column=1, padx=10, pady=5)
    
    # Drehmoment Eingabe
    tk.Label(manual_entry_window, text="Anfangswert Drehmoment:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    entry_start_drehmoment = tk.Entry(manual_entry_window)
    entry_start_drehmoment.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(manual_entry_window, text="Schrittweite Drehmoment:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
    entry_step_drehmoment = tk.Entry(manual_entry_window)
    entry_step_drehmoment.grid(row=4, column=1, padx=10, pady=5)
    
    tk.Label(manual_entry_window, text="Endwert Drehmoment:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
    entry_end_drehmoment = tk.Entry(manual_entry_window)
    entry_end_drehmoment.grid(row=5, column=1, padx=10, pady=5)
    
    tk.Button(manual_entry_window, text="Submit", command=on_submit).grid(row=6, column=0, columnspan=2, pady=10)

# Einstellungsfenster öffnen
def open_settings():
    def save_settings():
        global opcua_url, db_name, namespace_index, opcua_username, opcua_password
        opcua_url = url_entry.get()
        db_name = db_entry.get()
        namespace_index = int(ns_entry.get())
        opcua_username = user_entry.get()
        opcua_password = password_entry.get()
        messagebox.showinfo("Erfolg", "Einstellungen gespeichert")
        settings_window.destroy()

    settings_window = Toplevel(root)
    settings_window.title("Einstellungen")

    tk.Label(settings_window, text="OPC-UA Server URL:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    url_entry = tk.Entry(settings_window)
    url_entry.grid(row=0, column=1, padx=10, pady=5)
    url_entry.insert(0, opcua_url)
    
    tk.Label(settings_window, text="Datenbank Name:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    db_entry = tk.Entry(settings_window)
    db_entry.grid(row=1, column=1, padx=10, pady=5)
    db_entry.insert(0, db_name)
    
    tk.Label(settings_window, text="Namespace Index:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    ns_entry = tk.Entry(settings_window)
    ns_entry.grid(row=2, column=1, padx=10, pady=5)
    ns_entry.insert(0, str(namespace_index))
    
    tk.Label(settings_window, text="OPC-UA Username:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    user_entry = tk.Entry(settings_window)
    user_entry.grid(row=3, column=1, padx=10, pady=5)
    user_entry.insert(0, opcua_username)
    
    tk.Label(settings_window, text="OPC-UA Password:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
    password_entry = tk.Entry(settings_window, show="*")
    password_entry.grid(row=4, column=1, padx=10, pady=5)
    password_entry.insert(0, opcua_password)
    
    tk.Button(settings_window, text="Speichern", command=save_settings).grid(row=5, column=0, columnspan=2, pady=10)

# Daten sortieren nach Drehzahl
def sort_by_drehzahl():
    global daten
    if daten is None:
        messagebox.showerror("Fehler", "Keine Daten zum Sortieren vorhanden.")
        return

    try:
        daten = daten.sort_values(by=['drehzahl']).reset_index(drop=True)
        display_data(daten)
        messagebox.showinfo("Erfolg", "Daten nach Drehzahl sortiert")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Sortieren der Daten: {e}")

# Daten sortieren nach Drehmoment
def sort_by_drehmoment():
    global daten
    if daten is None:
        messagebox.showerror("Fehler", "Keine Daten zum Sortieren vorhanden.")
        return

    try:
        daten = daten.sort_values(by=['drehmoment']).reset_index(drop=True)
        display_data(daten)
        messagebox.showinfo("Erfolg", "Daten nach Drehmoment sortiert")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Sortieren der Daten: {e}")

# Hauptprogramm
if __name__ == "__main__":
    client = None

    root = tk.Tk()
    root.title("CSV zu OPC-UA")

    # Verbindung herstellen Button
    btn_connect = tk.Button(root, text="Mit OPC-UA Server verbinden", command=connect_to_server)
    btn_connect.pack(pady=10)

    # CSV hochladen Button
    btn_upload = tk.Button(root, text="CSV Datei hochladen", command=upload_csv)
    btn_upload.pack(pady=10)

    # Daten manuell eingeben Button
    btn_manual_entry = tk.Button(root, text="Daten direkt eingeben", command=enter_data_manually)
    btn_manual_entry.pack(pady=10)

    # Text Widget zum Anzeigen der CSV-Daten
    text_widget = scrolledtext.ScrolledText(root, width=80, height=20)
    text_widget.pack(pady=10)

    # Daten senden Button
    btn_send = tk.Button(root, text="Daten an SPS senden", command=send_to_sps)
    btn_send.pack(pady=10)

    # Sortier Buttons
    btn_sort_drehzahl = tk.Button(root, text="Nach Drehzahl sortieren", command=sort_by_drehzahl)
    btn_sort_drehzahl.pack(pady=5)

    btn_sort_drehmoment = tk.Button(root, text="Nach Drehmoment sortieren", command=sort_by_drehmoment)
    btn_sort_drehmoment.pack(pady=5)

    # Verbindung trennen Button
    btn_disconnect = tk.Button(root, text="Von OPC-UA Server trennen", command=disconnect_from_server)
    btn_disconnect.pack(pady=10)

    # Einstellungen Button
    btn_settings = tk.Button(root, text="Einstellungen", command=open_settings)
    btn_settings.pack(pady=10)

    # Beenden Button
    btn_exit = tk.Button(root, text="Beenden", command=root.quit)
    btn_exit.pack(pady=10)

    root.mainloop()
