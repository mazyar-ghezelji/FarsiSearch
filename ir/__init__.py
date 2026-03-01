"""
Information Retrieval System for the Hamshahri corpus (Persian).

A complete IR pipeline: preprocessing, inverted index, TF-IDF scoring,
and evaluation (precision, recall, F1, MAP).
"""

__version__ = "0.1.0"

from ir.preprocess import PersianPreprocessor
from ir.index import InvertedIndex
from ir.query import process_query_tokens
from ir.scoring import score_documents
from ir.evaluation import load_judgements, evaluate_ranking

__all__ = [
    "__version__",
    "PersianPreprocessor",
    "InvertedIndex",
    "process_query_tokens",
    "score_documents",
    "load_judgements",
    "evaluate_ranking",
]
