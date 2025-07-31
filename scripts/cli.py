# scripts/cli.py
import argparse
from pubmed_cli.fetcher import fetch_pubmed_ids, fetch_pubmed_details
from pubmed_cli.parser import parse_pubmed_xml
from pubmed_cli.filters import filter_by_year, filter_pharma_papers
from pubmed_cli.exporter import to_csv

def main():
    parser = argparse.ArgumentParser(
        description="Fetch and filter PubMed papers (e.g., pharma/biotech authored)"
    )
    parser.add_argument("query", help="PubMed search query")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "-f", "--file", help="Save results to a CSV file instead of printing to console"
    )
    parser.add_argument(
        "--start-year", type=int, help="Filter papers published from this year onwards"
    )
    parser.add_argument(
        "--end-year", type=int, help="Filter papers published up to this year"
    )
    parser.add_argument(
        "--pharma-only", action="store_true", help="Include only papers with pharma/biotech affiliations"
    )

    args = parser.parse_args()

    # --- Debug Info ---
    if args.debug:
        print(f" Query: {args.query}")
        print(f" Output: {args.file if args.file else 'Console'}")
        print(f" Year filter: {args.start_year or 'Any'} - {args.end_year or 'Any'}")
        if args.pharma_only:
            print(" Pharma-only filter: Enabled")

    # --- Fetch Paper IDs ---
    ids = fetch_pubmed_ids(args.query, retmax=50)
    if args.debug:
        print(f" Found {len(ids)} PubMed IDs: {ids}")

    if not ids:
        print(" No papers found for this query.")
        return

    # --- Fetch XML for those IDs ---
    xml_data = fetch_pubmed_details(ids)

    # --- Parse XML into structured dicts ---
    papers = parse_pubmed_xml(xml_data)

    if args.debug:
        print(f" Parsed {len(papers)} papers from PubMed XML.")

    # --- Apply Year Filter ---
    papers = filter_by_year(papers, args.start_year, args.end_year)

    # --- Apply Pharma Filter if requested ---
    if args.pharma_only:
        papers = filter_pharma_papers(papers)
        if args.debug:
            print(f" Filtered to {len(papers)} pharma/biotech papers.")

    # --- Output results ---
    if args.file:
        to_csv(papers, args.file)
        print(f" Saved {len(papers)} papers to {args.file}")
    else:
        print(f"\n {len(papers)} papers found:")
        for p in papers:
            print(f"- {p.get('title', 'Untitled')} ({p.get('pub_date', 'No Date')})")

if __name__ == "__main__":
    main()
