"""fetcher.py

Handles PubMed API calls via Entrez (NCBI).
Provides:
1) fetch_pubmed_ids(query)       -> List of PubMed IDs
2) fetch_pubmed_details(ids)     -> PubMed XML string
3) fetch_papers(query)           -> Raw MEDLINE text (legacy use)
"""

from Bio import Entrez
from typing import List

# Required by NCBI — replace with user email for production use
Entrez.email = "chaahatlokhande@gmail.com"

def fetch_pubmed_ids(query: str, retmax: int = 50) -> List[str]:
    """
    Fetch PubMed IDs for a search query.
    """
    handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
    results = Entrez.read(handle)
    handle.close()
    return results.get("IdList", [])

def fetch_pubmed_details(ids: List[str]) -> str:
    """
    Fetch PubMed details for a list of IDs (returns XML).
    """
    if not ids:
        return ""

    handle = Entrez.efetch(db="pubmed", id=",".join(ids), rettype="xml", retmode="text")
    xml_data = handle.read()
    handle.close()
    return xml_data

def fetch_papers(query: str, max_results: int = 50) -> str:
    """
    Legacy function: Fetch paper metadata as MEDLINE text.
    """
    ids = fetch_pubmed_ids(query, retmax=max_results)
    if not ids:
        return ""

    handle = Entrez.efetch(db="pubmed", id=",".join(ids), rettype="medline", retmode="text")
    medline_data = handle.read()
    handle.close()
    return medline_data