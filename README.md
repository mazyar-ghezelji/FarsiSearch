# FarsiSearch 🔍

> A Persian-language information retrieval system built on the Hamshahri corpus

---

## Overview

FarsiSearch is a full information retrieval (IR) pipeline implemented in Python, designed specifically for Persian (Farsi) text. It processes the [Hamshahri corpus](http://dbrg.ut.ac.ir/Hamshahri/) — a large collection of real-world Persian newspaper articles — and supports end-to-end document indexing, query processing, and relevance ranking.

The project addresses the unique challenges of Persian NLP: right-to-left script, rich morphology, character encoding variations, and the lack of whitespace-based word boundaries in some contexts.

---

## Features

- **Persian text preprocessing** — normalization, tokenization, and stemming using [`hazm`](https://github.com/sobhe/hazm)
- **Stop word filtering** — removes high-frequency Persian words that don't contribute to relevance
- **Inverted index construction** — efficient term-to-document mapping for fast retrieval
- **TF-IDF / BM25 ranking** — scores documents by relevance to a given query
- **Query execution** — accepts Persian queries and returns ranked results

---

## Dataset: Hamshahri Corpus

| Property | Details |
|---|---|
| Source | Hamshahri newspaper (Iran) |
| Language | Persian (Farsi) |
| Size | 160,000+ articles |
| Topics | Politics, economics, sports, culture, and more |
| Notable use | CLEF 2008 & 2009 Persian IR evaluation campaigns |

---

## Project Structure

```
FarsiSearch/
├── ir.ipynb               # Main notebook — full IR pipeline
├── HamshahriData.7z       # Compressed corpus data
├── Project Description.pdf  # Project spec and requirements
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.7+
- 7-Zip (to extract corpus data)

### Installation

```bash
# Clone the repository
git clone https://github.com/mazyar-ghezelji/FarsiSearch.git
cd FarsiSearch

# Install dependencies
pip install jupyter numpy pandas hazm

# Extract the corpus
7z x HamshahriData.7z
```

### Running

```bash
jupyter notebook ir.ipynb
```

Run the notebook cells in order to:
1. Load and preprocess the Hamshahri corpus
2. Build the inverted index
3. Execute Persian search queries
4. View ranked retrieval results

---

## Persian NLP Challenges

Working with Persian text requires special handling that differs significantly from English IR:

- **Right-to-left script** — text direction must be accounted for in processing pipelines
- **Morphological complexity** — words inflect heavily; stemming is essential for recall
- **Character variants** — Arabic and Persian share Unicode ranges but differ in some characters (e.g., ک vs ك, ی vs ي)
- **Compound words** — Persian frequently joins words that would be separate in English

This project uses `hazm` to handle these issues robustly.

---

## Dependencies

| Package | Purpose |
|---|---|
| `hazm` | Persian text normalization, tokenization, stemming |
| `numpy` | Numerical operations for TF-IDF vectors |
| `pandas` | Data handling for corpus documents |
| `jupyter` | Interactive notebook environment |

---

## References

- [Hamshahri Corpus — University of Tehran DBRG](http://dbrg.ut.ac.ir/Hamshahri/)
- [hazm — Persian NLP Library](https://github.com/sobhe/hazm)
- CLEF 2008 & 2009 — Persian track evaluation campaigns

---

## Author

**Mazyar Ghezelji**  
[github.com/mazyar-ghezelji](https://github.com/mazyar-ghezelji)
