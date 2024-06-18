from ..helpers.hubspot import HubspotConnectorApi, Endpoints
from ..helpers.get_dataframe import get_dataframe

from pprint import pprint

from typing import Optional
import pandas as pd
import requests

class BaseReadOne():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 object_endpoint: Endpoints,
                 record_id:int,
                 archived: bool = False,
                 properties: list = [],
                 associations:list = []):
        
        self.client = client
        self.object_endpoint = object_endpoint
        self.record_id = record_id
        self.archived = archived
        self.properties = properties
        self.associations = associations


    def call(self) -> requests.Response:
        
        querystring = {"archived":self.archived,'properties':self.properties,'associations': self.associations}
        response = requests.request("GET", f"{self.client.endpoint(self.object_endpoint)}/{self.record_id}", headers=self.client.headers, params=querystring)

        return response
    
    def get_properties(self) -> Optional[pd.DataFrame]:

        rq = self.call()
        pprint(rq.json())
        
        if rq.status_code == 200:
            return pd.json_normalize(rq.json())
        else:
            return None
    
    def get_associations(self):
        rq = self.call()