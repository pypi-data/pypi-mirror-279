
import requests
import json

class UserProfileSolrUtils:
    def __init__(self,client = None) -> None:
        self.solr_client = client
        self.solrSession = requests.Session()
        super().__init__()

    def get_user_identities(self,user_id:int):
        resp = self.solr_client.search(q=f'id:user_{user_id}',fl='id,identity_maps')
        data = resp.docs

        identities = []
        if data:
            try:
                identities =  json.loads(data[0]['identity_maps'][0])
            except KeyError:
                identities = []
            except Exception as e:
                identities = []
        return identities
    
    def get_user_skills(self,user_id:int):
        resp = self.solr_client.search(q=f'id:user_{user_id}',fl='id,skill_maps')
        data = resp.docs
        skills = []
        if data:
            try:
                skills =  json.loads(data[0]['skill_maps'][0])
            except KeyError:
                skills = []
        return skills
    
    def get_user_langs(self,user_id:int):
        resp = self.solr_client.search(q=f'id:user_{user_id}',fl='id,language_maps')
        data = resp.docs
        langs = []
        if data:
            try:
                langs =  json.loads(data[0]['language_maps'][0])
            except Exception:
                langs = []
        return langs
    
    def get_user_work_experience(self,user_id:int):
        resp = self.solr_client.search(q=f'id:user_{user_id}',fl='id,experience')
        data = resp.docs
        experience = []
        if data:
            try:
                experience =  json.loads(data[0]['experience'][0])
            except KeyError:
                experience = []
        return experience
    
    

    def commit_solr(self):
        self.solrclient.commit()
    
    def session_close(self):
        self.solrSession.close()


    
