"""Query processing: tokenization, wildcard expansion, vocabulary filter."""

from __future__ import unicode_literals

import re
from typing import Any

from hazm import word_tokenize

from ir.preprocess import PersianPreprocessor


def expand_wildcard(term: str, vocabulary: set[str]) -> list[str]:
    """Expand a wildcard term (e.g. 'سال*') to matching vocabulary terms."""
    if "*" not in term:
        return []
    pattern = term.strip() + "$"
    pattern = pattern.replace("*", r"\w+")
    regex = re.compile(pattern)
    return [s for s in vocabulary if regex.match(s)]


def process_query_tokens(
    query: str,
    preprocessor: PersianPreprocessor,
    dictionary: dict[str, Any],
) -> tuple[list[str], list[str]]:
    """
    Tokenize query, expand wildcards, stem/lemmatize, and filter to terms in index.
    Returns (unique_terms_in_index, full_query_term_list) for TF-IDF.
    """
    tokens = word_tokenize(preprocessor.normalize(query))
    vocabulary = set(dictionary.keys())
    expanded = []
    rest = []
    for a in tokens:
        if "*" in a:
            expanded.extend(expand_wildcard(a, vocabulary))
        else:
            rest.append(a)
    modified = preprocessor.process_tokens(rest) + expanded
    unique = list(dict.fromkeys(m for m in modified if m in dictionary))
    full = [m for m in modified if m in dictionary]
    return unique, full
