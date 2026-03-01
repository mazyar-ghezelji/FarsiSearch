"""Inverted index with positional postings for the Hamshahri corpus."""

from __future__ import unicode_literals

import pickle
from pathlib import Path
from typing import Any

from ir.config import DEFAULT_CORPUS_DIR, DEFAULT_CORPUS_YEARS, DEFAULT_INDEX_PATH, DEFAULT_STOP_WORDS_TOP_N
from ir.preprocess import PersianPreprocessor


# Index format: dict[term, [total_tf, dict[doc_id, [doc_tf, [positions]]]]]
IndexDict = dict[str, list[Any]]


class InvertedIndex:
    """
    Inverted index: term -> (total_tf, { doc_id -> (doc_tf, [positions]) }).
    """

    def __init__(self, preprocessor: PersianPreprocessor | None = None):
        self.preprocessor = preprocessor or PersianPreprocessor()
        self.dictionary: IndexDict = {}
        self.docs_count = 0
        self.docs_size: dict[str, int] = {}
        self._sorted_terms_by_freq: list[tuple[str, int]] | None = None

    def _add_document(self, doc_id: str, text: str) -> None:
        tokens = self.preprocessor.tokenize(text)
        size = len(tokens)
        self.docs_size[doc_id] = size
        self.docs_count += 1
        for pos, t in enumerate(tokens, start=1):
            term = self.preprocessor.process_token(t)
            if term in self.dictionary:
                self.dictionary[term][0] += 1
                postings = self.dictionary[term][1]
                if doc_id in postings:
                    postings[doc_id][0] += 1
                    postings[doc_id][1].append(pos)
                else:
                    postings[doc_id] = [1, [pos]]
            else:
                self.dictionary[term] = [1, {doc_id: [1, [pos]]}]
        self._sorted_terms_by_freq = None

    def remove_stop_words(self, top_n: int = DEFAULT_STOP_WORDS_TOP_N) -> None:
        """Remove the top-N most frequent terms (stop words)."""
        if self._sorted_terms_by_freq is None:
            self._sorted_terms_by_freq = sorted(
                [(t, self.dictionary[t][0]) for t in self.dictionary],
                key=lambda x: x[1],
            )
        for i in range(-top_n, 0):
            if i >= -len(self._sorted_terms_by_freq):
                term = self._sorted_terms_by_freq[i][0]
                if term in self.dictionary:
                    self.dictionary.pop(term, None)

    def build_from_corpus(
        self,
        corpus_dir: Path = DEFAULT_CORPUS_DIR,
        years: tuple[int, ...] = DEFAULT_CORPUS_YEARS,
        remove_stop_words: bool = True,
        stop_words_top_n: int = DEFAULT_STOP_WORDS_TOP_N,
    ) -> None:
        """Build index from Hamshahri corpus directories 2003..2007."""
        self.dictionary = {}
        self.docs_count = 0
        self.docs_size = {}
        self._sorted_terms_by_freq = None
        # years 2003..2007 -> range(3, 8)
        for i in range(3, 8):
            path = corpus_dir / f"200{i}"
            if not path.exists():
                continue
            for filepath in sorted(path.iterdir()):
                if not filepath.is_file():
                    continue
                doc_id = filepath.name
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()
                self._add_document(doc_id, text)
        if remove_stop_words:
            self.remove_stop_words(stop_words_top_n)

    def add_document(self, doc_id: str, text: str) -> None:
        """Add a single document to the index."""
        self._add_document(doc_id, text)

    def remove_document(self, doc_id: str) -> None:
        """Remove a document from the index."""
        self.docs_count -= 1
        self.docs_size.pop(doc_id, None)
        for term in list(self.dictionary.keys()):
            if doc_id in self.dictionary[term][1]:
                self.dictionary[term][1].pop(doc_id)
                if not self.dictionary[term][1]:
                    self.dictionary.pop(term)
        self._sorted_terms_by_freq = None

    def save(self, path: Path | str = DEFAULT_INDEX_PATH) -> None:
        """Persist index and metadata to pickle."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "dictionary": self.dictionary,
            "docs_count": self.docs_count,
            "docs_size": self.docs_size,
        }
        with open(path, "wb") as f:
            pickle.dump(data, f)

    def load(self, path: Path | str = DEFAULT_INDEX_PATH) -> None:
        """Load index from pickle."""
        path = Path(path)
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.dictionary = data["dictionary"]
        self.docs_count = data["docs_count"]
        self.docs_size = data["docs_size"]
        self._sorted_terms_by_freq = None
