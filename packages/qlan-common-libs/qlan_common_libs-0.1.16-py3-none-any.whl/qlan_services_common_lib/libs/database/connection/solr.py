#Instantiate Solr
import pysolr

def get_solr_client(solr_url:str):
    return  pysolr.Solr(solr_url, always_commit=False, timeout=15)