# PubMed Paper Fetcher

A command-line tool to fetch **research papers from PubMed** based on a user query and identify papers with **at least one author affiliated with a pharmaceutical or biotech company**.

The results can be printed to the console or saved to a CSV file.

---

## Features

✅ Fetches papers from **PubMed API** using full query syntax                                                                                                               
✅ Filters papers to detect **non-academic authors** and **company affiliations** (pharma/biotech)      
✅ Outputs to **console** or **CSV file**      
✅ Optional **debug mode** to show API flow and intermediate data      
✅ Built with **Poetry** for dependency management & packaging      

---

##  Code Structure

```
pubmed-paper-fetcher/
│
├── pubmed_paper_fetcher/
│   ├── fetcher.py        # API calls to PubMed (ESearch & EFetch)
│   ├── filters.py        # Parsing XML & identifying non-academic/company authors
│   ├── utils.py          # CSV saving utility
│   └── __init__.py
│
├── scripts/
│   ├── cli.py            # CLI entry point
│   └── __init__.py
│
├── pyproject.toml        # Poetry config (dependencies, CLI command)
├── README.md             # Documentation
└── ...
```

---

##  Installation

### Clone repo

```bash
git clone https://github.com/<your-username>/pubmed-paper-fetcher.git
cd pubmed-paper-fetcher
```

### Install dependencies

```bash
poetry install
```

---

## Usage

Run the CLI command:

```bash
poetry run get-papers-list "<your-query>"
```

### Options:

```
-d, --debug           Enable debug output
-f, --file <name>     Save results to CSV (instead of printing to console)
-h, --help            Show help message
```

### Examples

**1. Print to console**

```bash
poetry run get-papers-list "cancer immunotherapy" -d
```

**2. Save to CSV**

```bash
poetry run get-papers-list "cancer immunotherapy" -d -f results.csv
```

Will generate `results.csv` with columns:

* PubmedID
* Title
* Publication Date
* Non-academic Authors
* Company Affiliations
* Corresponding Author Email

---

## How Non-Academic Authors & Company Affiliations Are Identified

* Affiliations containing words like `university`, `college`, `institute`, or `hospital` are treated as **academic**.
* Affiliations containing keywords like `pharma`, `biotech`, `inc`, `ltd`, `corp`, or `therapeutics` are treated as **company affiliations**.

---

## Tools Used

* **[Poetry](https://python-poetry.org/)** – Dependency management & packaging
* **[Requests](https://docs.python-requests.org/)** – API calls to PubMed
* **[xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)** – Parsing PubMed XML
* **ChatGPT (OpenAI)** – Used for code scaffolding & structuring ideas

---

## Future Improvements

* More advanced affiliation detection (ML-based classification)
* Better handling of partial/missing metadata
* Publishing the module to TestPyPI

---
