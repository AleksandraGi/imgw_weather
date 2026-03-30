import requests
import pandas as pd


API_URL = "http://danepubliczne.imgw.pl/api/data/hydro/"

def get_hydro_data():
    """
    Fetches JSON data from IMGW public API.
    Returns a list of station data if successful, or None if occurs an error.
    """
    try:
        resp = requests.get(API_URL, timeout=5)   # Timeout after 5 seconds
        resp.raise_for_status()                         # Raise an exception for HTTP errors
        return resp.json()                              # Return JSON data as list
    except requests.RequestException as e:
        print("Błąd pobierania danych:", e)
        return None

def prepare_hydro_dataframe(data):
    """
    Converts the raw JSON into Pandas DataFrame and renames columns.
    """
    df = pd.DataFrame(data)

    df.rename(columns={'id_stacji':'ID stacji', 'stacja':'Stacja', 'rzeka':'Rzeka', 'wojewodztwo':'Województwo', 'lon':'Długość geograficzna', 'lat':'Szerokość geograficzna',
                       'stan_wody':'Stan wody', 'stan_wody_data_pomiaru':'Data pomiaru stanu wody', 'temperatura_wody':'Temperatura wody', 'temperatura_wody_data_pomiaru':'Data pomiaru temperatury wody',
                       'przeplyw':'Przepływ', 'przeplyw_data':'Data pomiaru przepływu', 'zjawisko_lodowe':'Zjawisko lodowe', 'zjawisko_lodowe_data_pomiaru':'Data pomiaru zjawiska lodowego', 
                       'zjawisko_zarastania':'Zjawisko zarastania', 'zjawisko_zarastania_data_pomiaru':'Data pomiaru zjawiska zarastania'}, inplace=True)
    # print(df["Stacja"].is_unique)   # check if all station names are unique (probably won't)
    # df.set_index("Stacja", inplace=True)
    # cities = sorted(df.index.tolist())

    cities = df['Stacja'].tolist()

    return df, cities



raw_data = prepare_hydro_dataframe(get_hydro_data())



def create_gui(x):
    pass


def main():
    """
    Main function that downloads data, prepare it and launch GUI.
    """
    data = get_hydro_data()
    if data:
        df, cities, columns = get_hydro_data(data)
        create_gui(df, cities, columns)

if __name__=="__main__":
    main()
