"""parser.py

Handles parsing of MEDLINE (BioPython) or PubMed XML into normalized dicts.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List

def parse_medline_record(record: dict) -> Dict:
    """
    Parse a single BioPython MEDLINE record into a normalized dict.
    Used when using BioPython's Entrez + Medline pipeline.
    """
    return {
        "pmid": record.get("PMID", ""),
        "title": record.get("TI", ""),
        "abstract": record.get("AB", ""),
        "authors": record.get("AU", []),
        "affiliations": record.get("AD", []),  # may be a list or single string
        "journal": record.get("JT", ""),
        "doi": record.get("LID", "").replace(" [doi]", "") if "LID" in record else "",
        "pub_date": record.get("DP", "")
    }

def parse_pubmed_xml(xml: str) -> List[Dict]:
    """
    Parse PubMed XML returned by the EFetch API (requests-based pipeline).
    Extracts key metadata into a normalized dictionary format.
    """
    root = ET.fromstring(xml)
    parsed_papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or article.findtext(".//PubDate/MedlineDate")

        authors = []
        affiliations = []

        for author in article.findall(".//Author"):
            name = (author.findtext("LastName") or "") + " " + (author.findtext("ForeName") or "")
            if name.strip():
                authors.append(name.strip())
            # collect all affiliations for this author
            for aff in author.findall(".//Affiliation"):
                if aff.text:
                    affiliations.append(aff.text.strip())

        parsed_papers.append({
            "pmid": pmid,
            "title": title,
            "pub_date": pub_date,
            "authors": authors,
            "affiliations": affiliations
        })

    return parsed_papers