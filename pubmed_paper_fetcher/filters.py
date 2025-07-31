# pubmed_paper_fetcher/filters.py
import xml.etree.ElementTree as ET
from typing import List, Dict

ACADEMIC_KEYWORDS = ["university", "college", "institute", "hospital"]
COMPANY_KEYWORDS = ["pharma", "biotech", "inc", "ltd", "corp", "corporation", "therapeutics"]

def is_non_academic(affiliation: str) -> bool:
    """Check if affiliation is non-academic."""
    return not any(word in affiliation.lower() for word in ACADEMIC_KEYWORDS)

def is_company_affiliation(affiliation: str) -> bool:
    """Check if affiliation looks like pharma/biotech company."""
    return any(word in affiliation.lower() for word in COMPANY_KEYWORDS)

def parse_pubmed_xml(xml: str) -> List[Dict]:
    """Parse PubMed XML and extract required fields."""
    root = ET.fromstring(xml)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or article.findtext(".//PubDate/MedlineDate")

        non_academic_authors = []
        company_affiliations = []
        corresponding_email = None

        for author in article.findall(".//Author"):
            name = (author.findtext("LastName") or "") + " " + (author.findtext("ForeName") or "")
            affiliations = [aff.text for aff in author.findall(".//Affiliation") if aff.text]

            for aff in affiliations:
                if is_non_academic(aff):
                    non_academic_authors.append(name.strip())
                if is_company_affiliation(aff):
                    company_affiliations.append(aff.strip())
                if "@" in aff and not corresponding_email:
                    corresponding_email = aff.strip()

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Authors": "; ".join(set(non_academic_authors)),
            "Company Affiliations": "; ".join(set(company_affiliations)),
            "Corresponding Author Email": corresponding_email or ""
        })

    return papers

def filter_by_year(papers: list[dict], start_year: int = None, end_year: int = None) -> list[dict]:
    """Filter papers based on year range."""
    if not start_year and not end_year:
        return papers

    filtered = []
    for paper in papers:
        year = paper.get("year")
        if year:
            if (not start_year or int(year) >= start_year) and (not end_year or int(year) <= end_year):
                filtered.append(paper)
    return filtered