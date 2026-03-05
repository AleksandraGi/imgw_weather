# https://danepubliczne.imgw.pl
# https://danepubliczne.imgw.pl/pl/apiinfo
# aktualne:  temperatura ; prędkość wiatru ; kierunek wiatru ; wilgotność względna ; suma opadów ; ciśnienie
# wypisać stacje do wyboru, napisać datę i godzinę pomiaru oraz wybrany parametr 

import requests
import pandas as pd
import tkinter as tk
from tkinter import ttk

API_URL = "https://danepubliczne.imgw.pl/api/data/synop"  

def download_data():
    """
    Fetches JSON data from IMGW public API.
    Returns a list of station data if successful, or None if occurs an error.
    """
    try:
        resp = requests.get(API_URL, timeout=5)     # Timeout after 5 seconds
        resp.raise_for_status()                     # Raise an exception for HTTP errors
        return resp.json()                          # Return JSON data as list
    except requests.RequestException as e:
        print("Błąd pobierania danych:", e)
        return None


def prepare_dataframe(data):
    """
    Converts the raw JSON into Pandas DataFrame and renames columns.
    """
    df = pd.DataFrame(data)
    df.rename(columns={'id_stacji':'ID stacji', 'stacja':'Stacja', 'data_pomiaru':'Data pomiaru', 
                       'godzina_pomiaru':'Godzina pomiaru', 'temperatura':'Temperatura', 'predkosc_wiatru':'Prędkość wiatru',
                       'kierunek_wiatru':'Kierunek wiatru', 'wilgotnosc_wzgledna':'Wilgotność względna', 
                       'suma_opadu':'Suma opadu', 'cisnienie':'Ciśnienie'}, inplace=True)
    # df.set_index("Stacja", inplace=True)      # CHECK ONE DAY
    cities = df['Stacja'].tolist()
    weather_columns = ["Temperatura", "Prędkość wiatru", "Kierunek wiatru", "Wilgotność względna", "Suma opadu", "Ciśnienie"]
    return df, cities, weather_columns


def create_gui(df, cities, columns):
    """
    Creates the Tkinter GUI for selecting a city and weather parameter.
    Displays values when button is clicked
    """
    # ------------------ WINDOW ------------------
    root = tk.Tk()
    root.title("Weather App")
    root.geometry("400x300")
    root.resizable(False, False)

    # ------------------ CITY ------------------
    tk.Label(root, text="Choose city:").pack(pady=(15, 5))              # Label for city selection
    city_combobox = ttk.Combobox(root, values=cities, state="readonly") # Combobox to select city
    city_combobox.current(0) 
    city_combobox.pack(pady=10)

    # ------------------ PARAMETER ------------------
    tk.Label(root, text="Choose parametr:").pack(pady=(15, 5))              # Label for parametr selection
    param_combobox = ttk.Combobox(root, values=columns, state="readonly")   # Combobox to select parametr
    param_combobox.current(0) 
    param_combobox.pack(pady=10)

   # ------------------ RESULT ------------------
    result_label = tk.Label(root, text="", wraplength=380, justify="center")    # Label for result
    result_label.pack()

    # ------------------ BUTTON ------------------
    def show_value():
        """
        Reads selected city and parameter from comboboxes.
        Retrives data from DataFrame.
        Updates result label.
        """
        city = city_combobox.get()
        param = param_combobox.get()

        # row with values for that station
        row = df[df["Stacja"] == city]
        date = row.iloc[0]["Data pomiaru"]
        hour = row.iloc[0]["Godzina pomiaru"]

        if not row.empty:
            value = row.iloc[0][param]
            result_label.config(text=f"{city} {date} {hour}\n{param}: {value}")
        else:
            result_label.config(text=f"Brak danych")

    button = tk.Button(root, text="Get value", command=show_value)
    button.pack(pady=10)
    root.mainloop()


def main():
    """
    Main function that downloads data, prepare it and launch GUI.
    """
    data = download_data()
    if data:
        df, cities, columns = prepare_dataframe(data)
        create_gui(df, cities, columns)

if __name__=="__main__":
    main()




"""
TO DO:

1)
sort alfabetically cities ()
    WEATHER_COLUMNS = [
        "Temperatura",
        "Prędkość wiatru",
        "Kierunek wiatru",
        "Wilgotność względna",
        "Suma opadu",
        "Ciśnienie"
    df.set_index("Stacja", inplace=True)  # Use station name as index for easy lookup
    cities = sorted(df.index.tolist())  # Alphabetically sort city names

2) Different text for different parameters: units (opady w mm, temperatrura w stopniach Celsjusza, wiatr rysunek)

3) Add languages


"""