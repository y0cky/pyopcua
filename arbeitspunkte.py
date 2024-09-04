import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd

# Standardwerte
default_speed_start = 100
default_speed_end = 2500
default_speed_step = 100

default_torque_start = 5
default_torque_end = 70
default_torque_step = 5

default_torque_limitations = {
    1200: 65,
    1300: 60,
    1400: 55,
    1500: 50,
    1600: 45,
    1700: 40,
    1800: 40,
    1900: 35,
    2000: 35,
    2100: 30,
    2200: 30,
    2300: 25,
    2400: 25,
    2500: 25,
}

df_global = None

def generate_and_show_table():
    global df_global
    # Eingabewerte aus der GUI holen
    speed_start = int(speed_start_var.get())
    speed_end = int(speed_end_var.get())
    speed_step = int(speed_step_var.get())
    
    torque_start = int(torque_start_var.get())
    torque_end = int(torque_end_var.get())
    torque_step = int(torque_step_var.get())

    # Drehzahlbereich und Drehmomentbereich erstellen
    speeds = range(speed_start, speed_end + speed_step, speed_step)
    torques = range(torque_start, torque_end + torque_step, torque_step)

    # Begrenzung der Maximalwerte des Drehmoments bei hohen Drehzahlen
    torque_limitations = {}
    for entry in torque_limits_var.get().split(','):
        speed, limit = map(int, entry.split('='))
        torque_limitations[speed] = limit

    # Erstelle eine leere Liste für die Tabelle
    table_data = []

    # Generiere die Tabelle
    for torque in torques:
        row = [torque]
        for n in speeds:
            # Begrenze das Drehmoment, wenn eine Begrenzung für die Drehzahl existiert
            limited_torque = min(torque, torque_limitations.get(n, torque))
            row.append((n, limited_torque))
        table_data.append(row)

    # Erstelle ein DataFrame
    columns = ["n/M"] + list(speeds)
    df_global = pd.DataFrame(table_data, columns=columns)

    # Tabelle in neuem Fenster anzeigen
    show_table()

def show_table():
    if df_global is not None:
        # Neues Fenster erstellen
        table_window = tk.Toplevel(root)
        table_window.title("Erzeugte Tabelle")

        # Erstelle ein Treeview-Widget
        tree = ttk.Treeview(table_window, columns=list(df_global.columns), show='headings')

        # Spaltenüberschriften hinzufügen
        for col in df_global.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor='center')

        # Daten hinzufügen
        for index, row in df_global.iterrows():
            tree.insert('', 'end', values=list(row))

        # Scrollbars hinzufügen
        vsb = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(table_window, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Packen der Widgets
        tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')

def save_csv():
    if df_global is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Tabelle speichern")
        if file_path:
            df_global.to_csv(file_path, index=False)

def save_list_as_csv():
    if df_global is not None:
        # Wähle die Sortierreihenfolge
        sort_order = sort_order_var.get()
        
        # Erstelle eine leere Liste für die Daten
        list_data = []

        # Fülle die Liste mit den Werten aus der Tabelle
        for _, row in df_global.iterrows():
            torque = row["n/M"]
            for n, torque_value in zip(df_global.columns[1:], row[1:]):
                list_data.append([torque_value[1], n])
        
        # Erstelle ein DataFrame für die Liste
        list_df = pd.DataFrame(list_data, columns=["Drehmoment", "Drehzahl"])

        # Sortiere die Liste basierend auf der Auswahl
        if sort_order == "torque_first":
            list_df = list_df.sort_values(by=["Drehmoment", "Drehzahl"])
        else:
            list_df = list_df.sort_values(by=["Drehzahl", "Drehmoment"])

        # Füge eine fortlaufende Index-Spalte hinzu, beginnend bei 0
        list_df.reset_index(drop=True, inplace=True)
        list_df.index.name = 'Index'

        # Speichere die Liste als CSV-Datei
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Liste speichern")
        if file_path:
            list_df.to_csv(file_path, index=True)

# Erstelle die Hauptanwendung
root = tk.Tk()
root.title("Arbeitspunkte Generator")

# GUI Layout
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Drehzahlbereich-Einstellungen
tk.Label(frame, text="Drehzahlbereich (min^-1)").grid(row=0, column=0, columnspan=2)
tk.Label(frame, text="Start:").grid(row=1, column=0, sticky=tk.E)
tk.Label(frame, text="Ende:").grid(row=2, column=0, sticky=tk.E)
tk.Label(frame, text="Schrittweite:").grid(row=3, column=0, sticky=tk.E)

speed_start_var = tk.StringVar(value=str(default_speed_start))
speed_end_var = tk.StringVar(value=str(default_speed_end))
speed_step_var = tk.StringVar(value=str(default_speed_step))

tk.Entry(frame, textvariable=speed_start_var).grid(row=1, column=1)
tk.Entry(frame, textvariable=speed_end_var).grid(row=2, column=1)
tk.Entry(frame, textvariable=speed_step_var).grid(row=3, column=1)

# Drehmomentbereich-Einstellungen
tk.Label(frame, text="Drehmomentbereich (Nm)").grid(row=4, column=0, columnspan=2)
tk.Label(frame, text="Start:").grid(row=5, column=0, sticky=tk.E)
tk.Label(frame, text="Ende:").grid(row=6, column=0, sticky=tk.E)
tk.Label(frame, text="Schrittweite:").grid(row=7, column=0, sticky=tk.E)

torque_start_var = tk.StringVar(value=str(default_torque_start))
torque_end_var = tk.StringVar(value=str(default_torque_end))
torque_step_var = tk.StringVar(value=str(default_torque_step))

tk.Entry(frame, textvariable=torque_start_var).grid(row=5, column=1)
tk.Entry(frame, textvariable=torque_end_var).grid(row=6, column=1)
tk.Entry(frame, textvariable=torque_step_var).grid(row=7, column=1)

# Feldschwächebereich-Einstellungen
tk.Label(frame, text="Feldschwächebereich (Drehmomentbegrenzung)").grid(row=8, column=0, columnspan=2)
tk.Label(frame, text="Drehzahlen=Begrenzung (z.B. 1200=65,1300=60)").grid(row=9, column=0, columnspan=2)

torque_limits_var = tk.StringVar(value="1200=65,1300=60,1400=55,1500=50,1600=45,1700=40,1800=40,1900=35,2000=35,2100=30,2200=30,2300=25,2400=25,2500=25")

tk.Entry(frame, textvariable=torque_limits_var, width=50).grid(row=10, column=0, columnspan=2)

# Kombinierter Button zur Tabellengenerierung und -anzeige
generate_and_show_button = tk.Button(frame, text="Tabelle generieren und anzeigen", command=generate_and_show_table)
generate_and_show_button.grid(row=11, column=0, columnspan=2, pady=10)

# Button zum Speichern der Tabelle als CSV
save_button = tk.Button(frame, text="Tabelle als CSV speichern", command=save_csv)
save_button.grid(row=12, column=0, columnspan=2, pady=5)

# Auswahl der Sortierreihenfolge
sort_order_var = tk.StringVar(value="torque_first")
tk.Label(frame, text="Sortierreihenfolge für CSV:").grid(row=13, column=0, columnspan=2, pady=10)
tk.Radiobutton(frame, text="Drehmoment > Drehzahl", variable=sort_order_var, value="torque_first").grid(row=14, column=0, columnspan=2)
tk.Radiobutton(frame, text="Drehzahl > Drehmoment", variable=sort_order_var, value="speed_first").grid(row=15, column=0, columnspan=2)

# Button zum Speichern der Liste als CSV
save_list_button = tk.Button(frame, text="Liste als CSV speichern", command=save_list_as_csv)
save_list_button.grid(row=16, column=0, columnspan=2, pady=5)

# Starte die Hauptanwendung
root.mainloop()
