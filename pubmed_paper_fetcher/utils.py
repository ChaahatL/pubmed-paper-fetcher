# pubmed_paper_fetcher/utils.py
import csv
from typing import List, Dict

def save_to_csv(papers: List[Dict], filename: str):
    """Save parsed paper data to a CSV file."""
    if not papers:
        print(" No papers to save.")
        return
    
    keys = papers[0].keys()  # column names
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(papers)
    print(f" Saved {len(papers)} papers to {filename}")
