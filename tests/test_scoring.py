"""Tests for TF-IDF scoring and evaluation metrics."""

from __future__ import unicode_literals

import math
import pytest
from ir.scoring import score_documents, SCORE_LNN_LTN, SCORE_LNC_LTC
from ir.evaluation import f_measure, average_precision, evaluate_ranking


def test_f_measure():
    assert f_measure(0.5, 0.5) == pytest.approx(0.5)
    assert f_measure(1.0, 1.0) == pytest.approx(1.0)
    assert f_measure(0.0, 0.0) == 0.0


def test_average_precision():
    assert average_precision([0.5, 1.0]) == pytest.approx(0.75)
    assert average_precision([]) == 0.0


def test_evaluate_ranking_empty_relevant():
    scores = [("d1", 1.0), ("d2", 0.5)]
    m = evaluate_ranking(scores, [])
    assert m["precision"] == 0.0
    assert m["recall"] == 0.0
    assert m["f1"] == 0.0
    assert m["map"] == 0.0


def test_evaluate_ranking_perfect():
    scores = [("d1", 1.0), ("d2", 0.5)]
    m = evaluate_ranking(scores, ["d1", "d2"])
    assert m["precision"] == 1.0
    assert m["recall"] == 1.0
    assert m["f1"] == pytest.approx(1.0)
    assert m["map"] == pytest.approx(1.0)


def test_score_documents_empty_terms():
    d = {}
    ds = {}
    scores = score_documents(d, ds, 0, [], [], mode=SCORE_LNN_LTN)
    assert scores == []


def test_score_documents_single_term():
    # Minimal index: one term "a" in doc "d1", doc length 2; query has "a" twice so TF>0
    dictionary = {"a": [2, {"d1": [2, [1, 2]]}]}
    docs_size = {"d1": 2}
    docs_count = 1
    terms = ["a"]
    full = ["a", "a"]
    scores = score_documents(dictionary, docs_size, docs_count, terms, full, mode=SCORE_LNN_LTN)
    assert len(scores) == 1
    assert scores[0][0] == "d1"
    assert scores[0][1] >= 0
