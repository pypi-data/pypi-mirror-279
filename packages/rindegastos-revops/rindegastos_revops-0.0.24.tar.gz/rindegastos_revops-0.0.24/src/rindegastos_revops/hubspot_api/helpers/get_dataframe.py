import pandas as pd
import requests

def get_dataframe(response:requests.Response) -> pd.DataFrame:
    # Verificamos la existencia de los resultados
    response_json = response.json()
    df = pd.json_normalize(response_json, record_path="results", sep="_")
    return df

def next_page(dict:dict):
    if "paging" in dict.keys():
        print(dict["paging"])
        after = dict["paging"]["next"]["after"]
        return after
    return None
