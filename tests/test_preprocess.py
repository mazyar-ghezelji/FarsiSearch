"""Tests for Persian preprocessing."""

from __future__ import unicode_literals

import pytest
from ir.preprocess import PersianPreprocessor


def test_preprocessor_normalize():
    p = PersianPreprocessor()
    out = p.normalize("  متن   تست  ")
    assert isinstance(out, str)


def test_preprocessor_tokenize():
    p = PersianPreprocessor()
    tokens = p.tokenize("سلام دنیا")
    assert isinstance(tokens, list)
    assert len(tokens) >= 1


def test_preprocessor_process_token():
    p = PersianPreprocessor()
    t = p.process_token("مازیار")
    assert isinstance(t, str)
