from ..helpers.hubspot import HubspotConnectorApi, Endpoints, ObjectTypeId
from ..helpers.get_dataframe import next_page

from .associations import Associations

from typing import Optional
import pandas as pd
import requests


class BaseRead():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 object_endpoint: Endpoints,
                 archived: bool = False,
                 properties: list = [],
                 associations:list = []):
        
        self.client = client
        self.object_endpoint = object_endpoint
        self.archived = archived
        self.properties = properties
        self.associations = associations


    def call(self, after:Optional[str] = None, limit:int = 100) -> requests.Response:
        
        querystring = {"limit":limit,"archived":self.archived,'properties':self.properties,'associations':self.associations}
        if after:
            querystring["after"] = after

        response = requests.request("GET"
                                    ,self.client.endpoint(self.object_endpoint)
                                    ,headers=self.client.headers
                                    ,params=querystring)
        
        # Si la respuesta es None entonces se acaba la consulta
        if response.status_code != 200:
            return None
        
        return response

    def get_properties_and_associations(self, response:dict):
        results = response["results"]

        properties, associations = [], []
        for record in results:
            properties.append(record["properties"])
            
            if "associations" in record.keys():
                assosiation_dict = record["associations"]
                assosiation_dict["record_id"] = record["id"]
                associations.append(assosiation_dict)

        return properties, associations

    def rq_normalize(self, test:bool = True, test_iterations:int = 1) -> tuple[list, list]:
        after = None
        iterations = 0

        properties, associations = [], []
        while True:
            rq = self.call(after)

            if rq.status_code == 200:
                response=rq.json()
                #Se obtiene la siguiente página de ser necesario
                after=next_page(response)

                #Se obtienen las propiedades del grupo de registros
                records_properties, records_associations=self.get_properties_and_associations(response)
                #Se agregan las propiedades al grupo supremo de registros
                properties.extend(records_properties)
                associations.extend(records_associations)

                #pprint(response)
                iterations+=1
            else:
                return "A ocurrido un error al momento de hacer el request"
            
            test_filter = test and iterations>=test_iterations
            if after == None or test_filter:
                break
        
        return properties, associations
