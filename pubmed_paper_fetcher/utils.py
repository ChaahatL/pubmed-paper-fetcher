# pubmed_paper_fetcher/utils.py
import csv
from typing import List, Dict

def save_to_csv(papers: List[Dict], filename: str):
    """Save parsed paper data to a CSV file with EXACT required headers and order."""
    if not papers:
        print(" No papers to save.")
        return

    # Define exact headers as per requirement
    headers = [
        "PubmedID",
        "Title",
        "Publication Date",
        "Non-academic Author(s)",
        "Company Affiliation(s)",
        "Corresponding Author Email"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for paper in papers:
            writer.writerow({
                "PubmedID": paper.get("pmid", ""),
                "Title": paper.get("title", ""),
                "Publication Date": paper.get("pub_date", ""),
                "Non-academic Author(s)": ", ".join(paper.get("non_academic_authors", [])),
                "Company Affiliation(s)": ", ".join(paper.get("company_affiliations", [])),
                "Corresponding Author Email": paper.get("corresponding_email", "")
            })

    print(f" Saved {len(papers)} papers to {filename} with required format.")
