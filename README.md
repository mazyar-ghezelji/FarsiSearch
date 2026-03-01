# Information Retrieval System

A comprehensive information retrieval system implementation in Python for the Hamshahri corpus (Persian language).

## Overview

This project implements a complete information retrieval system designed to process and search through Persian-language documents from the Hamshahri corpus. The system demonstrates key IR concepts including document indexing, query processing, and relevance ranking for Persian text.

## About the Hamshahri Corpus

The Hamshahri Corpus is a substantial Persian text collection derived from the Hamshahri newspaper, one of Iran's earliest online Persian-language newspapers. The collection comprises over 160,000 articles spanning various subjects including politics, economics, sports, literature, and more, with documents ranging from brief news items to extensive articles.

### Corpus Details
- **Source**: Hamshahri newspaper articles
- **Language**: Persian (Farsi)
- **Content**: News articles from various categories
- **Use Case**: A standard reliable Persian text collection used at the Cross Language Evaluation Forum (CLEF) in 2008 and 2009 for evaluating Persian information retrieval systems

## Repository Contents

- **`ir.ipynb`**: Main Jupyter notebook containing the IR system implementation
- **`HamshahriData.7z`**: Compressed archive containing the Hamshahri corpus data
- **`Project Description.pdf`**: Detailed project documentation and requirements

## Features

This information retrieval system likely includes:

- **Text Preprocessing**: Tokenization and normalization for Persian text
- **Indexing**: Building inverted indices for efficient document retrieval
- **Query Processing**: Handling user queries in Persian language
- **Ranking**: Implementing relevance ranking algorithms (e.g., TF-IDF, BM25)
- **Search Interface**: Query execution and result presentation

## Requirements

- Python 3.8+
- Dependencies: `jupyter`, `numpy`, `pandas`, `hazm` (see `requirements.txt`).

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mazyar-ghezelji/information-retrieval-system.git
cd information-retrieval-system
```

2. Extract the corpus data:
```bash
7z x HamshahriData.7z
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Launch Jupyter Notebook:
```bash
jupyter notebook ir.ipynb
```

2. Run the cells sequentially to:
   - Load and preprocess the Hamshahri corpus
   - Build the inverted index
   - Execute search queries
   - Evaluate retrieval performance

## Implementation Approach

The system addresses Persian-language specific challenges:

- **Right-to-Left Text**: Proper handling of Persian script direction
- **Morphological Complexity**: Persian word stemming and normalization
- **Character Variations**: Managing different forms of Persian characters
- **Stop Words**: Filtering common Persian words that don't contribute to relevance

## Applications

This IR system can be used for:

- Academic research in Persian information retrieval
- Building search engines for Persian content
- Text mining and analysis of Persian documents
- Educational purposes for learning IR concepts
- Baseline system for evaluating Persian IR algorithms

## Performance Considerations

The Persian language requires special considerations in IR system design due to its distinct characteristics compared to languages like English. This implementation takes into account Persian-specific linguistic features for optimal retrieval performance.

## References

For more information about the Hamshahri corpus and Persian information retrieval:

- [Hamshahri Collection Official Site](http://dbrg.ut.ac.ir/Hamshahri/)
- Persian@CLEF 2008 and 2009 evaluation campaigns
- Research papers on Persian text processing and IR

## Making this repo better

Ideas for future improvements:

- **Refactor into a Python package**: Move indexing, query processing, and evaluation into modules (e.g. `preprocess.py`, `index.py`, `query.py`, `evaluation.py`) and keep the notebook as a thin runner. This improves testability and reuse.
- **Configurable paths**: Use a config file (YAML/JSON) or environment variables for corpus path, corpus years (e.g. `2003`–`2007`), and query/judgement paths so others can run without editing the notebook.
- **Safe file I/O**: Use `with open(...) as f:` for all file and pickle operations to avoid resource leaks.
- **Fix list mutation during iteration**: Replace `for a in modified_tokens: ... modified_tokens.remove(a)` with a list comprehension so you don’t modify a list while iterating (e.g. `modified_tokens = [a for a in modified_tokens if a in dictionary]`).
- **Add tests**: Unit tests for preprocessing (tokenization, stemming), scoring (TF-IDF, cosine), and evaluation (precision, recall, F1, MAP) to guard against regressions.
- **Add BM25**: Implement BM25 ranking as an alternative to TF-IDF for better robustness.
- **CLI**: Optional `python -m ir index` and `python -m ir search --query "..."` for indexing and search without opening the notebook.
- **Index persistence**: Document the pickle format and optionally add version/checks when saving/loading the index.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the system.

## License

This project is open source and available for academic and research purposes.

## Author

Mazyar Ghezelji

## Acknowledgments

- University of Tehran DBRG Group for creating and maintaining the Hamshahri corpus
- The Persian NLP research community
- CLEF (Cross Language Evaluation Forum) for standardizing Persian IR evaluation

---

**Note**: For detailed implementation specifics and methodology, please refer to the `Project Description.pdf` file included in the repository.
