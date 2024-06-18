from ..helpers.hubspot import HubspotConnectorApi, ObjectTypeId
from ..helpers.get_dataframe import next_page

from typing import Optional
import pandas as pd
import requests


class Associations():
    def __init__(self,
                 client:HubspotConnectorApi 
                 ,object_type_id:ObjectTypeId
                 ,associations:list
                 ,rq_rs_associations:list[dict]):
        
        self.client = client
        self.object_type_id = object_type_id
        self.associations = associations
        self.rq_rs_associations = rq_rs_associations

    def association_list(self, object_id, to_object_type:ObjectTypeId, after:Optional[str] = None, limit:int = 500):

        querystring = {"limit":limit}
        if after:
            querystring["after"] = after

        url = f"https://api.hubapi.com/crm/v4/objects/{self.object_type_id.value}/{object_id}/associations/{to_object_type.value}"
        response = requests.request("GET"
                                    ,url
                                    ,headers=self.client.headers
                                    ,params=querystring)
                
        # Si la respuesta es None entonces se acaba la consulta
        if response.status_code != 200:
            return None
        
        return response

    def get_associations(self, response:dict):
        results = response["results"]
        associations = []

        for record in results:
            association_record = {'id':record["toObjectId"], "typeId":record["associationTypes"][0]["typeId"]}
            associations.append(association_record)

        return associations
    
    def rq_normalize(self, object_id, to_object_type):
        after = None
        
        associations = []
        while True:
            rq = self.association_list(object_id
                                       ,to_object_type
                                       ,after)
                    
            if rq.status_code == 200:
                response=rq.json()
                #Se obtiene la siguiente página de ser necesario
                after=next_page(response)

                records_associations=self.get_associations(response)

                associations.extend(records_associations)
            
            if after == None:
                break

        return associations

    def proccess_associations(self, to_object_type_id:ObjectTypeId):
        response_list = []
        to_object_name = to_object_type_id.name.lower()

        for associations_record in self.rq_rs_associations:
            if not to_object_name in associations_record.keys():
                continue
            
            if "paging" in associations_record[to_object_name].keys():
                associations=self.rq_normalize(associations_record["record_id"]
                                               ,to_object_type_id)
            else:
                associations=associations_record[to_object_name]["results"]
            
            response = {"record_id":associations_record["record_id"],to_object_name:associations}
            response_list.append(response)

        return response_list
    
    def get_association_df(self, to_object_type_id:ObjectTypeId):

        if not to_object_type_id.value in self.associations:
            return f"El objeto {to_object_type_id.name} no se encuentra en la lista de asociaciones"

        object_name = self.object_type_id.name.lower()
        to_object_name = to_object_type_id.name.lower()
        
        object_associations = self.proccess_associations(to_object_type_id)

        if object_associations == []:
            return f"No existen asociaciones del tipo {self.object_type_id.name}-{to_object_type_id.name} en los registros extraidos"
        
        object_association_table = pd.json_normalize(object_associations
                                                     ,to_object_name, ["record_id"])
        
        object_name_id = f'{object_name[:-1]}_id'
        to_object_name_id = f'{to_object_name[:-1]}_id'

        rename_columns = {'id':to_object_name_id, 'record_id':object_name_id}
        output_association_table = object_association_table.rename(columns=rename_columns)


        return output_association_table[[object_name_id, to_object_name_id]]