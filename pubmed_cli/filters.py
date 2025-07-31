"""filters.py

Filtering logic for pharma/biotech papers vs academic ones, plus date filtering.
"""

from typing import List, Dict
from pubmed_cli.constants import PHARMA_KEYWORDS, ACADEMIC_KEYWORDS

def is_pharma_affiliation(affiliation: str) -> bool:
    """Check if an affiliation looks like pharma/biotech company."""
    return any(word.lower() in affiliation.lower() for word in PHARMA_KEYWORDS)

def is_academic_affiliation(affiliation: str) -> bool:
    """Check if an affiliation looks like an academic institution."""
    return any(word.lower() in affiliation.lower() for word in ACADEMIC_KEYWORDS)

def filter_pharma_papers(papers: List[Dict]) -> List[Dict]:
    """
    Return only papers where at least one affiliation matches pharma/biotech.
    """
    pharma_papers = []
    for paper in papers:
        if any(is_pharma_affiliation(aff) for aff in paper.get("affiliations", [])):
            pharma_papers.append(paper)
    return pharma_papers

def filter_academic_papers(papers: List[Dict]) -> List[Dict]:
    """
    Return only papers where at least one affiliation matches academic institutions.
    """
    academic_papers = []
    for paper in papers:
        if any(is_academic_affiliation(aff) for aff in paper.get("affiliations", [])):
            academic_papers.append(paper)
    return academic_papers

def filter_by_year(papers: list[dict], start_year: int = None, end_year: int = None) -> list[dict]:
    """Filter papers based on year range. 
    
    - If no filters are provided, return ALL papers (even those missing a year).
    - If filters are provided, only include papers with a year that matches.
    """
    # If no filter is applied, don’t drop anything
    if not start_year and not end_year:
        return papers  

    filtered = []
    for paper in papers:
        year_str = paper.get("pub_date")

        # If paper has no date, skip filtering (we can either drop it OR keep it)
        # Decision: DROP it because user specifically requested a year filter
        if not year_str:
            continue  

        try:
            year = int(year_str[:4])  # handles YYYY-MM-DD too
        except ValueError:
            continue  # skip if year is malformed

        if (not start_year or year >= start_year) and (not end_year or year <= end_year):
            filtered.append(paper)

    return filtered
