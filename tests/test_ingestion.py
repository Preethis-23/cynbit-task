"""
Tests for DocumentParser and schemas.
"""

import pytest
from src.ingestion.parser import DocumentParser, IngestionError


def test_parse_plain_text():
    parser = DocumentParser()
    sample = "We need an e-commerce platform with login, catalog, and Stripe payment."
    doc = parser.parse_plain_text(sample, source_type="text", filename="sample.txt")
    assert doc.metadata.source_type == "text"
    assert doc.metadata.word_count > 5
    assert "e-commerce" in doc.cleaned_text


def test_empty_text_error():
    parser = DocumentParser()
    with pytest.raises(IngestionError):
        parser.parse_plain_text("")


def test_text_normalization():
    parser = DocumentParser()
    dirty = "Line 1\r\n\r\n\r\n\r\nLine 2   \u00a0with spaces\n"
    normalized = parser.normalize_text(dirty)
    assert "\r" not in normalized
    assert "\n\n\n" not in normalized
    assert "with spaces" in normalized


def test_parse_file_txt():
    parser = DocumentParser()
    raw = b"Sample project brief for testing parser dispatcher."
    doc = parser.parse_file(raw, "test.txt")
    assert doc.metadata.source_type == "text"
    assert doc.metadata.filename == "test.txt"
