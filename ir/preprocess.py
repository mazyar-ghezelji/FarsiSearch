"""Persian text preprocessing using Hazm."""

from __future__ import unicode_literals

from hazm import Normalizer, Stemmer, Lemmatizer, word_tokenize


class PersianPreprocessor:
    """Normalize, tokenize, stem, and lemmatize Persian text."""

    def __init__(self):
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.lemmatizer = Lemmatizer()

    def normalize(self, text: str) -> str:
        return self.normalizer.normalize(text)

    def tokenize(self, text: str) -> list[str]:
        return word_tokenize(self.normalize(text))

    def process_token(self, token: str) -> str:
        """Stem and lemmatize a single token."""
        return self.lemmatizer.lemmatize(self.stemmer.stem(token))

    def process_tokens(self, tokens: list[str]) -> list[str]:
        """Process a list of tokens (stem + lemmatize)."""
        return [self.process_token(t) for t in tokens]
