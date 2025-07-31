"""Basic tests for fetcher module (with mocked Entrez)."""

import io
import pytest
from pubmed_cli import fetcher

@pytest.fixture
def mock_entrez(monkeypatch):
    """Fixture to mock BioPython Entrez API methods."""

    class MockHandle(io.StringIO):
        def close(self):  # override close so pytest doesn't error
            super().close()

    def mock_esearch(db, term, retmax):
        assert db == "pubmed"
        return MockHandle('{"IdList": ["12345", "67890"]}')  # JSON-like string for Entrez.read()

    def mock_efetch(db, id, rettype, retmode):
        assert db == "pubmed"
        if rettype == "xml":
            return MockHandle("<PubmedArticleSet><PubmedArticle><PMID>12345</PMID></PubmedArticle></PubmedArticleSet>")
        elif rettype == "medline":
            return MockHandle("PMID- 12345\nTI  - Mock title\n")

    def mock_read(handle):
        # Entrez.read usually parses the handle into dict
        return {"IdList": ["12345", "67890"]}

    # Patch Entrez functions
    monkeypatch.setattr(fetcher.Entrez, "esearch", mock_esearch)
    monkeypatch.setattr(fetcher.Entrez, "efetch", mock_efetch)
    monkeypatch.setattr(fetcher.Entrez, "read", mock_read)

    return monkeypatch

def test_fetch_pubmed_ids(mock_entrez):
    ids = fetcher.fetch_pubmed_ids("CRISPR", retmax=5)
    assert ids == ["12345", "67890"]

def test_fetch_pubmed_details(mock_entrez):
    xml_data = fetcher.fetch_pubmed_details(["12345"])
    assert "<PMID>12345</PMID>" in xml_data

def test_fetch_papers_medline(mock_entrez):
    medline_data = fetcher.fetch_papers("Cancer")
    assert "PMID- 12345" in medline_data
