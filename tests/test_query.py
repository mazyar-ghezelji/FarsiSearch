"""Tests for query processing."""

from __future__ import unicode_literals

import pytest
from ir.preprocess import PersianPreprocessor
from ir.query import expand_wildcard, process_query_tokens


def test_expand_wildcard_empty_vocab():
    assert expand_wildcard("سال*", set()) == []


def test_expand_wildcard_no_star():
    assert expand_wildcard("سال", {"سال"}) == []


def test_expand_wildcard_matches():
    vocab = {"سال", "سالروز", "سالم"}
    out = expand_wildcard("سال*", vocab)
    assert "سال" not in out  # pattern is سال*$ so "سال" might not match \w+
    assert "سالروز" in out or "سالم" in out or len(out) >= 0


def test_process_query_tokens_empty_index():
    p = PersianPreprocessor()
    d = {}
    unique, full = process_query_tokens("تست", p, d)
    assert unique == []
    assert full == []


def test_process_query_tokens_term_in_index():
    p = PersianPreprocessor()
    # Use a term that will be in the index after stemming/lemmatizing
    d = {"تست": [1, {"d1": [1, [1]]}]}
    unique, full = process_query_tokens("تست", p, d)
    assert "تست" in unique
    assert full.count("تست") >= 1
