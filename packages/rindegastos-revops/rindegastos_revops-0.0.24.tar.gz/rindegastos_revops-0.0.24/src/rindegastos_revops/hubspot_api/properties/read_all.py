from ...hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints

import pandas as pd
from typing import Optional
import requests

def all_properties_df(client: HubspotConnectorApi, endpoint: Endpoints) -> Optional[pd.DataFrame]:
    response = requests.request("GET", client.endpoint(endpoint), headers=client.headers)

    if not response.status_code == 200:
        return None
    
    if response.status_code == 200:
        response_json = response.json()
    
    if not "results" in response_json.keys():
        return None
    
    df = pd.json_normalize(response_json, record_path="results", sep="_")

    return df