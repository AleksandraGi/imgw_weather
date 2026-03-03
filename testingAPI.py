# https://danepubliczne.imgw.pl
# https://danepubliczne.imgw.pl/pl/apiinfo

import requests
import json
import pandas as pd
import tkinter as tk
from tkinter import ttk

# aktualne:  temperatura ; prędkość wiatru ; kierunek wiatru ; wilgotność względna ; suma opadów ; ciśnienie
# wypisać stacje do wyboru
# napisać datę i godzinę pomiaru oraz wybrany parametr 



url = "https://danepubliczne.imgw.pl/api/data/synop"  # wszystkie stacje, JSON
resp = requests.get(url)
if resp.status_code == 200:
    data = resp.json()
    # wypisz pierwszą stację
    # print(data[0])
    df = pd.DataFrame(data)
    df.rename(columns={'id_stacji':'ID stacji', 'stacja':'Stacja', 'data_pomiaru':'Data pomiaru', 'godzina_pomiaru':'Godzina pomiaru', 'temperatura':'Temperatura', 'predkosc_wiatru':'Prędkość wiatru',
                       'kierunek_wiatru':'Kierunek wiatru', 'wilgotnosc_wzgledna':'Wilgotność względna', 'suma_opadu':'Suma opadu', 'cisnienie':'Ciśnienie'}, inplace=True)
    
    cities = df['Stacja'].tolist()
    columns = df.columns[5:].tolist()
    print(columns)

else:
    print("Błąd:", resp.status_code)



## WINDOW
def on_select(event):
    # Funkcja wywoływana po wybraniu opcji
    print(f"Wybrano: {combobox.get()}")

# Główne okno
root = tk.Tk()
root.title("WEATHER")
root.geometry("300x200")


## CHOOSING CITY
# Tworzenie ComboBox
# state="readonly" zapobiega wpisywaniu własnego tekstu przez użytkownika
combobox = ttk.Combobox(root, values=cities, state="readonly")
combobox.current(0)  # Ustawia domyślnie pierwszą opcję (indeks 0)
combobox.pack(pady=20)

# Wiązanie zdarzenia wyboru
combobox.bind("<<ComboboxSelected>>", on_select)

# Przycisk pobierający wartość
def get_value():
    print(f"Got with button: {combobox.get()}")

button = tk.Button(root, text="Get value", command=get_value)
button.pack()



## CHOOSING PARAMETRT
combobox = ttk.Combobox(root, values=columns, state="readonly")
combobox.current(0)  # Ustawia domyślnie pierwszą opcję (indeks 0)
combobox.pack(pady=20)

# Wiązanie zdarzenia wyboru
combobox.bind("<<ComboboxSelected>>", on_select)

# Przycisk pobierający wartość
def get_value2():
    print(f"Got with button: {combobox.get()}")

button = tk.Button(root, text="Get value", command=get_value2)
button.pack()

root.mainloop()






# ARCHIWUM

# # wybór stacji
# station_id = 12500
# url = f"https://danepubliczne.imgw.pl/api/data/synop/id/{station_id}"
# resp = requests.get(url)
# data = resp.json()
# print(data)
# print(data['temperatura'])




# wybór stacji, roku
# wykres i tabela porównująca opad i przepływ

# def get_all_synop():
#     url = "https://danepubliczne.imgw.pl/api/data/synop"
#     resp = requests.get(url)
#     resp.raise_for_status()
#     return resp.json()

# def get_station_by_id(station_id: int):
#     url = f"https://danepubliczne.imgw.pl/api/data/synop/id/{station_id}"
#     resp = requests.get(url)
#     resp.raise_for_status()
#     return resp.json()

# def save_to_file(data, fname="weather.json"):
#     with open(fname, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)

# if __name__ == "__main__":
#     # Pobierz dane wszystkich stacji
#     data = get_all_synop()
#     print(f"Pobrano {len(data)} rekordów.")
#     # print("Pierwsza stacja:", data[0])
#     save_to_file(data, "all_synop.json")

#     # Pobierz dane dla stacji o konkretnym ID
#     station_id = 12345  
#     try:
#         st = get_station_by_id(station_id)
#         print("Dane stacji:", st)
#         save_to_file(st, f"station_{station_id}.json")
#     except requests.HTTPError as e:
#         print("Nie udało się pobrać danych dla stacji:", station_id, "->", e)





