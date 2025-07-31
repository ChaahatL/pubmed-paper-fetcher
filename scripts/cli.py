# scripts/cli.py
import argparse
from pubmed_paper_fetcher.fetcher import fetch_pubmed_details, fetch_pubmed_ids
from pubmed_paper_fetcher.filters import filter_by_year, parse_pubmed_xml
from pubmed_paper_fetcher.utils import save_to_csv

def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers with pharma/biotech authors"
    )
    parser.add_argument("query", help="PubMed search query")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "-f", "--file", help="Save results to a CSV file instead of printing"
    )
    parser.add_argument("--start-year", type=int, help="Filter papers published from this year onwards")
    parser.add_argument("--end-year", type=int, help="Filter papers published up to this year")

    args = parser.parse_args()

    if args.debug:
        print(f" Query: {args.query}")
        print(f" Output file: {args.file if args.file else 'Console'}")
        if args.start_year or args.end_year:
            print(f" Year filter: {args.start_year or 'Any'} - {args.end_year or 'Any'}")

    # 1️ Fetch papers
    ids = fetch_pubmed_ids(args.query, retmax=10)
    if args.debug:
        print(f" Found {len(ids)} papers: {ids}")

    xml_data = fetch_pubmed_details(ids)

    # 2️ Parse XML
    papers = parse_pubmed_xml(xml_data)

    # 3️ Apply filters (if any)
    papers = filter_by_year(papers, args.start_year, args.end_year)

    # 4️ Output
    if args.file:
        save_to_csv(papers, args.file)
        print(f" Saved {len(papers)} papers to {args.file}")
    else:
        print(f" {len(papers)} papers found:")
        for p in papers:
            print(f"- {p['Title']} ({p['Publication Date']})")