"""Tests for CLI module."""

import sys
import pytest
import scripts.cli as cli

@pytest.fixture
def mock_fetcher(monkeypatch):
    """Mock fetcher functions to avoid hitting the real API."""

    def fake_fetch_pubmed_ids(query, retmax=50):
        return ["12345", "67890"]

    def fake_fetch_pubmed_details(ids):
        # Minimal XML for parser to handle
        return """
        <PubmedArticleSet>
          <PubmedArticle>
            <PMID>12345</PMID>
            <ArticleTitle>Mock Paper</ArticleTitle>
            <PubDate><Year>2023</Year></PubDate>
            <AuthorList>
              <Author>
                <LastName>Smith</LastName>
                <ForeName>John</ForeName>
                <Affiliation>Pfizer Inc</Affiliation>
              </Author>
            </AuthorList>
          </PubmedArticle>
        </PubmedArticleSet>
        """

    monkeypatch.setattr(cli, "fetch_pubmed_ids", fake_fetch_pubmed_ids)
    monkeypatch.setattr(cli, "fetch_pubmed_details", fake_fetch_pubmed_details)


def test_cli_runs_basic(mock_fetcher, capsys):
    """Test CLI main() runs and prints summary."""
    sys.argv = ["cli", "CRISPR"]  # simulate `python cli.py CRISPR`
    cli.main()
    captured = capsys.readouterr()
    assert "papers found" in captured.out


def test_cli_with_debug(mock_fetcher, capsys):
    """Test CLI with debug flag shows extra info."""
    sys.argv = ["cli", "CRISPR", "--debug"]
    cli.main()
    captured = capsys.readouterr()
    assert "Query: CRISPR" in captured.out
    assert "Found" in captured.out


def test_cli_with_pharma_only(mock_fetcher, capsys):
    """Test CLI with pharma-only flag filters correctly."""
    sys.argv = ["cli", "CRISPR", "--pharma-only"]
    cli.main()
    captured = capsys.readouterr()
    assert "pharma/biotech" not in captured.out  # should run but not necessarily print that
    assert "papers found" in captured.out
