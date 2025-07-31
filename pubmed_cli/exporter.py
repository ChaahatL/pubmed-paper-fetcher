"""exporter.py

Handles exporting filtered papers to CSV with fixed headers.
"""

import csv
from typing import List, Dict

# Define consistent headers once here
CSV_HEADERS = [
    "PubmedID",
    "Title",
    "Publication Date",
    "Non-academic Author(s)",
    "Company Affiliation(s)",
    "Corresponding Author Email"
]

def to_csv(papers: List[Dict], filename: str) -> None:
    """Export papers to a CSV file with fixed headers."""
    if not papers:
        print("No papers to export.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
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

    print(f"Saved {len(papers)} papers to {filename}")