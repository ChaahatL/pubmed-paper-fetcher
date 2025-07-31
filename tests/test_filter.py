"""Tests for filter module."""

import pytest
from pubmed_cli import filters

def test_is_pharma_affiliation():
    assert filters.is_pharma_affiliation("Pfizer Inc, New York")
    assert filters.is_pharma_affiliation("Biotech Labs Ltd")
    assert not filters.is_pharma_affiliation("Harvard University")

def test_is_academic_affiliation():
    assert filters.is_academic_affiliation("Stanford University, USA")
    assert filters.is_academic_affiliation("Johns Hopkins Hospital")
    assert not filters.is_academic_affiliation("Merck Pharmaceuticals")

def test_filter_pharma_papers():
    papers = [
        {"affiliations": ["Pfizer Inc", "Harvard University"], "title": "Drug Study"},
        {"affiliations": ["Oxford University"], "title": "Cancer Research"}
    ]
    pharma_papers = filters.filter_pharma_papers(papers)
    assert len(pharma_papers) == 1
    assert pharma_papers[0]["title"] == "Drug Study"

def test_filter_academic_papers():
    papers = [
        {"affiliations": ["Pfizer Inc"], "title": "Drug Study"},
        {"affiliations": ["Stanford University"], "title": "Gene Therapy"}
    ]
    academic_papers = filters.filter_academic_papers(papers)
    assert len(academic_papers) == 1
    assert academic_papers[0]["title"] == "Gene Therapy"

def test_filter_by_year():
    papers = [
        {"title": "Old Study", "pub_date": "1998"},
        {"title": "Recent Study", "pub_date": "2022"},
        {"title": "No Date Study", "pub_date": ""}
    ]

    # Only after 2000
    recent = filters.filter_by_year(papers, start_year=2000)
    assert len(recent) == 1
    assert recent[0]["title"] == "Recent Study"

    # Only before 2010
    older = filters.filter_by_year(papers, end_year=2010)
    assert len(older) == 1
    assert older[0]["title"] == "Old Study"

    # No filters applied
    all_papers = filters.filter_by_year(papers)
    assert len(all_papers) == 3
