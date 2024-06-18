from ..helpers.hubspot import HubspotConnectorApi, ObjectTypeId
from typing import Optional
import requests
import pandas as pd


class Pipelines():
   
    def __init__(self, client:HubspotConnectorApi, object_type_id:ObjectTypeId) -> None:
         self.client = client
         self.object_type_id = object_type_id

    def retrieve_all_pipelines_request(self, after:Optional[str] = None, limit:int = 500):

        querystring = {"limit":limit}
        if after:
            querystring["after"] = after

        url = f"https://api.hubapi.com/crm/v3/pipelines/{self.object_type_id.value}"
        response = requests.request("GET"
                                    ,url
                                    ,headers=self.client.headers
                                    ,params=querystring)
                
        # Si la respuesta es None entonces se acaba la consulta
        if response.status_code != 200:
            return None
        
        return response
    
    def get_pipeline_stage(self, pipeline):

        stage_data = []
        for stage in pipeline["stages"]:
            id = stage["id"]
            created_at = stage["createdAt"]
            label = stage["label"]
            pipeline_id = pipeline["id"]

            stage_data.append([id, created_at, label, pipeline_id]) 

        return stage_data
            


    def get_pipelines(self):

        all_pipelines_request = self.retrieve_all_pipelines_request()
        if all_pipelines_request.status_code!=200:
            return "A ocurrido un error"
        
        all_pipelines_response:dict = all_pipelines_request.json()

        pipeline_data = []
        stage_data =[]

        pipeline_columns=["id","created_at","label"]
        stage_columns=["id","created_at","label", "pipeline_id"]

        if "results" in all_pipelines_response.keys():
            results = all_pipelines_response["results"]

            for pipeline in results:

                pipeline_data.append([pipeline["id"],pipeline["createdAt"],pipeline["label"]])

                pipeline_stage = self.get_pipeline_stage(pipeline)
                stage_data.extend(pipeline_stage)

        pipelines_df = pd.DataFrame(pipeline_data, columns=pipeline_columns)
        stages_df = pd.DataFrame(stage_data, columns=stage_columns)
        
        return pipelines_df, stages_df

     

            
            