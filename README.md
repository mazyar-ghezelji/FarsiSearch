# Information Retrieval System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A full information retrieval pipeline for the **Hamshahri corpus** (Persian): indexing, TF-IDF ranking, and evaluation (Precision, Recall, F1, MAP).

## Features

- **Persian NLP**: Tokenization, normalization, stemming, and lemmatization via [Hazm](https://github.com/roshan-research/hazm)
- **Inverted index**: Positional postings, configurable stop-word removal
- **Query processing**: Wildcard expansion (`سال*`), vocabulary filtering
- **Scoring**: TF-IDF with lnn.ltn or lnc.ltc (cosine) modes
- **Evaluation**: Judgements-based Precision, Recall, F1, MAP
- **CLI & API**: Command-line tools and importable Python package

## Project structure

```
.
├── ir/                    # Main package
│   ├── __init__.py
│   ├── config.py          # Paths and constants
│   ├── preprocess.py      # Persian preprocessing (Hazm)
│   ├── index.py           # Inverted index build/save/load
│   ├── query.py           # Query tokenization and wildcards
│   ├── scoring.py         # TF-IDF and cosine scoring
│   ├── evaluation.py      # Load judgements, P/R, F1, MAP
│   └── cli.py             # Command-line interface
├── tests/
├── ir.ipynb               # Original notebook (exploratory)
├── config.yaml            # Optional path overrides
├── pyproject.toml
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Requirements

- **Python 3.8+**
- Hazm, NumPy, Pandas (see `pyproject.toml`)

## Installation

```bash
git clone https://github.com/mazyar-ghezelji/information-retrieval-system.git
cd information-retrieval-system
pip install -e .
```

For development and the notebook:

```bash
pip install -e ".[dev,notebook]"
```

## Data

1. Extract the Hamshahri corpus (e.g. `7z x HamshahriData.7z`).
2. Expected layout:
   - `Documents/HamshahriData/HamshahriCorpus/2003/` … `2007/` (documents)
   - `Documents/HamshahriData/Queris/1.q` … `50.q` (queries)
   - `Documents/HamshahriData/RelativeAssesemnt/judgements.txt` (relevance judgements)

Paths can be overridden in `config.yaml` or via CLI flags.

## Usage

### Command line

**Build index:**

```bash
ir index --corpus Documents/HamshahriData/HamshahriCorpus --output dict.pickle
```

**Search:**

```bash
ir search "مازیار" --index dict.pickle --top-k 20
ir search "سال*" --cosine
```

**Evaluate on all 50 queries:**

```bash
ir evaluate --index dict.pickle --queries Documents/HamshahriData/Queris --judgements Documents/HamshahriData/RelativeAssesemnt/judgements.txt
```

### Python API

```python
from pathlib import Path
from ir import InvertedIndex, PersianPreprocessor, process_query_tokens, score_documents

# Build or load index
index = InvertedIndex()
index.build_from_corpus(Path("Documents/HamshahriData/HamshahriCorpus"))
# index.load("dict.pickle")

# Run a query
preprocessor = PersianPreprocessor()
terms, full = process_query_tokens("مازیار", preprocessor, index.dictionary)
scores = score_documents(
    index.dictionary, index.docs_size, index.docs_count,
    terms, full, mode="1"
)
for doc_id, score in scores[:10]:
    print(doc_id, score)
```

### Notebook

The original workflow is preserved in `ir.ipynb`. You can also use the package from the notebook:

```python
from ir import InvertedIndex, process_query_tokens, score_documents
# ... use as above
```

## Testing

```bash
pytest
pytest -v --cov=ir
```

## About the Hamshahri corpus

The [Hamshahri](http://dbrg.ut.ac.ir/Hamshahri/) corpus is a Persian text collection from the Hamshahri newspaper, used in CLEF 2008–2009 for evaluating Persian IR systems.

## License

MIT. See [LICENSE](LICENSE).

## Author

**Mazyar Ghezelji**

## Acknowledgments

- University of Tehran DBRG for the Hamshahri corpus
- CLEF and the Persian NLP community
