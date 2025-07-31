# 📄 **PubMed Paper Fetcher CLI**

A command-line tool to fetch research papers from **PubMed** based on a user query and identify papers with at least one author affiliated with a **pharmaceutical** or **biotech** company.

The results can be printed to the console or saved to a CSV file.

---

## ✨ Features

✅ Fetches papers from **PubMed API** using full query syntax      
✅ Filters papers to detect **non-academic authors** and **company affiliations (pharma/biotech)**    
✅ Outputs to **console** or **CSV file**    
✅ Optional **debug mode** to show API flow and intermediate data    
✅ Built with **Poetry** for dependency management & packaging    

---

## 📂 Project Structure

```
pubmed-cli-tool/
│
├── pubmed_cli/               # Core package
│   ├── fetcher.py            # PubMed API calls (Entrez E-utilities)
│   ├── filters.py            # Logic for parsing & identifying pharma/biotech authors
│   ├── utils.py              # CSV saving utilities
│   └── __init__.py
│
├── scripts/                  # CLI entry point
│   ├── cli.py                # Main CLI logic (argparse)
│   └── __init__.py
│
├── tests/                    # Pytest test suite
│   ├── test_cli.py
│   ├── test_fetcher.py
│   └── test_filter.py
│
├── dist/                     # (auto-generated) build artifacts for TestPyPI/PyPI
├── pyproject.toml            # Poetry config (dependencies, CLI command)
├── README.md                 # Documentation
└── ...
```

---

## 🔧 Installation (Developers)

Clone the repo & install dependencies:

```bash
git clone https://github.com/<your-username>/pubmed-cli-tool.git
cd pubmed-cli-tool
poetry install
```

Run tests to verify everything works:

```bash
poetry run pytest
```

---

## 🚀 Usage

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

---

### 📌 Examples

#### 1️⃣ Print to console:

```bash
poetry run get-papers-list "cancer immunotherapy" --debug
```

#### 2️⃣ Save to CSV:

```bash
poetry run get-papers-list "cancer immunotherapy" -f results.csv
```

This generates **`results.csv`** with columns:

* PubmedID
* Title
* Publication Date
* Non-academic Authors
* Company Affiliations
* Corresponding Author Email

---

## 🔍 How It Detects Pharma/Biotech Authors

* **Academic affiliations** (university, college, institute, hospital) are treated as academic.
* **Company affiliations** (pharma, biotech, inc, ltd, corp, therapeutics) are flagged as industry.

---

## 🛠 Tools & Libraries

* **Poetry** – Dependency management & packaging
* **Biopython** – PubMed API access (via `Bio.Entrez`)
* **Requests** – API calls
* **argparse** – CLI parsing
* **pytest** – Testing framework

---

## 📦 Future Improvements

* ML-based affiliation classification
* More robust handling of missing metadata
* Better CSV formatting options
* Continuous integration tests

---
