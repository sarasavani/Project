import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import yticks
import pandas as pd

def seconds_to_time_str(total_seconds):
    # Calcola ore, minuti, secondi e millisecondi
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)

    # Crea la stringa formattata, rimuovendo ore e minuti se sono 0
    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}.{milliseconds:03}"
    else:
        return f"{minutes}:{seconds:02}.{milliseconds:03}"

def time_to_seconds(time_str):
    """Converti un tempo stringa (mm:ss.SSS) in secondi float."""
    minutes, seconds = time_str.split(":")
    return int(minutes) * 60 + float(seconds)

def seconds_to_time(seconds):
    """Converti un tempo in secondi in formato stringa (mm:ss.SSS)."""
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes}:{seconds:.3f}"

#given the error string, print the error
def error(error_string) :
    print("Error! " + error_string)

#given the driverId, finds the row of the selected driver in drivers
#returns row, the row in which the driver is located (the dataset is a bit random with indexes)
def find_row_driver(driver_input,drivers) :
    row=0
    for d in drivers.iloc[:,0] :
        if driver_input==d:
            return row
        else: row=row+1
    error("driver not found")

def print_all_races(races):
        # Seleziona solo le colonne 'raceId', 'name' e 'year'
        races_info = races[['raceId', 'name', 'year']]
        pd.set_option('display.max_rows', None)

        # Stampa tutte le gare
        print(races_info.to_string(index=False))