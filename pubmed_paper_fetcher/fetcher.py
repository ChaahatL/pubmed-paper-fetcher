# pubmed_paper_fetcher/fetcher.py
import requests
from typing import List

PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_ids(query: str, retmax: int = 20) -> List[str]:
    """Fetch PubMed IDs for a given query using ESearch API."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax
    }
    response = requests.get(PUBMED_ESEARCH, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]

def fetch_pubmed_details(ids: List[str]) -> str:
    """Fetch details for a list of PubMed IDs using EFetch API (returns XML)."""
    ids_str = ",".join(ids)
    params = {
        "db": "pubmed",
        "id": ids_str,
        "retmode": "xml"
    }
    response = requests.get(PUBMED_EFETCH, params=params)
    response.raise_for_status()
    return response.text