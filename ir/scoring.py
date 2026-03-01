"""TF-IDF weighting and cosine scoring (lnn.ltn and lnc.ltc)."""

from __future__ import unicode_literals

import math
from typing import Any

# Scoring modes: 1 = lnn.ltn (no doc/query normalization), 2 = lnc.ltc (cosine)
SCORE_LNN_LTN = "1"
SCORE_LNC_LTC = "2"


def _tfidf_doc_weights(
    dictionary: dict[str, Any],
    docs_size: dict[str, int],
    docs_count: int,
    terms: list[str],
) -> dict[str, list[float]]:
    """Build document vectors: log(tf/doc_len). IDF applied later to query."""
    weights: dict[str, list[float]] = {}
    for word in dictionary:
        if word not in terms:
            continue
        idx = terms.index(word)
        for doc_id, (tf, _) in dictionary[word][1].items():
            if doc_id not in weights:
                weights[doc_id] = [0.0] * len(terms)
            size = docs_size.get(doc_id, 1)
            weights[doc_id][idx] = math.log10(tf / size) if size else 0.0
    return weights


def _tfidf_query_weights(
    terms: list[str],
    full_query_terms: list[str],
    dictionary: dict[str, Any],
    docs_count: int,
) -> list[float]:
    """Query vector: log(tf/len) * idf per term."""
    q = [0.0] * len(terms)
    n_query = len(full_query_terms) or 1
    for i, word in enumerate(terms):
        tf_q = full_query_terms.count(word)
        if tf_q == 0:
            continue
        q[i] = math.log10(tf_q / n_query)
        df = len(dictionary[word][1])
        idf = math.log10(docs_count / df) if df else 0.0
        q[i] *= idf
    return q


def _normalize_docs_cosine(weights: dict[str, list[float]], exclude: str = "query") -> None:
    """In-place: normalize each document vector by L2 norm (lnc.ltc)."""
    for doc_id, vec in weights.items():
        if doc_id == exclude:
            continue
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            for i in range(len(vec)):
                vec[i] /= norm


def score_documents(
    dictionary: dict[str, Any],
    docs_size: dict[str, int],
    docs_count: int,
    terms: list[str],
    full_query_terms: list[str],
    mode: str = SCORE_LNN_LTN,
) -> list[tuple[str, float]]:
    """
    Compute TF-IDF weights and return documents ranked by cosine similarity to query.
    mode '1': lnn.ltn (no normalization), '2': lnc.ltc (cosine normalization).
    """
    if not terms:
        return []
    weights = _tfidf_doc_weights(dictionary, docs_size, docs_count, terms)
    weights["query"] = _tfidf_query_weights(terms, full_query_terms, dictionary, docs_count)
    if mode == SCORE_LNC_LTC:
        _normalize_docs_cosine(weights)
    scores: list[tuple[str, float]] = []
    q = weights["query"]
    for doc_id, vec in weights.items():
        if doc_id == "query":
            continue
        score = sum(a * b for a, b in zip(vec, q))
        scores.append((doc_id, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores
