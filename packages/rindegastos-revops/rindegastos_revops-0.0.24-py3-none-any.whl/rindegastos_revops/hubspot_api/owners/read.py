from ..helpers.hubspot import HubspotConnectorApi, ObjectTypeId, Endpoints
from typing import Optional
import requests
import pandas as pd
from ..helpers.get_dataframe import next_page


class Owners():
   
    def __init__(self, client:HubspotConnectorApi) -> None:
         self.client = client

    def get_owners_request(self, archived:bool, after:Optional[str] = None, limit:int = 100):

        querystring = {"limit":limit,"archived":archived}

        if after:
            querystring["after"] = after

        response = requests.request("GET"
                                    ,self.client.endpoint(Endpoints.OWNERS)
                                    ,headers=self.client.headers
                                    ,params=querystring)
                
        # Si la respuesta es None entonces se acaba la consulta
        if response.status_code != 200:
            return None
        
        return response
    
    def get_owner_info(self, response):
        owner_data = []

        results = response["results"]

        for record in results:
            owner_record = [record["id"],record["createdAt"],record["email"],record["firstName"],record["lastName"],record["userIdIncludingInactive"],record["archived"]]
            owner_data.append(owner_record)

        return owner_data
    
    def request_normalize(self, archived:bool) -> list:
        after = None

        data = []
        while True:
            rq = self.get_owners_request(archived, after)

            if rq.status_code == 200:
                response=rq.json()
                #Se obtiene la siguiente página de ser necesario
                after=next_page(response)
                #Se obtienen las propiedades del grupo de registros
                ownners_records =self.get_owner_info(response)
                #Se agregan las propiedades al grupo supremo de registros
                data.extend(ownners_records)
            else:
                return "A ocurrido un error al momento de hacer el request"
            
            if after == None:
                break

        
        return data
    
    def get_dataframe(self, archived:bool):
        owners_response = self.request_normalize(archived)
        columns = ["id_propietario","fecha_creacion","email","nombre","apellido","id_usuario","archivado"]

        return pd.DataFrame(owners_response, columns=columns)