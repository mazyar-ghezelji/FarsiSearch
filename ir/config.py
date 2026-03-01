"""Runtime configuration with defaults and optional YAML override."""

from pathlib import Path

# Default paths relative to project root or cwd
DEFAULT_CORPUS_DIR = Path("Documents/HamshahriData/HamshahriCorpus")
DEFAULT_QUERIES_DIR = Path("Documents/HamshahriData/Queris")
DEFAULT_JUDGEMENTS_PATH = Path("Documents/HamshahriData/RelativeAssesemnt/judgements.txt")
DEFAULT_INDEX_PATH = Path("dict.pickle")

# Corpus years to index (Hamshahri folders 2003..2007)
DEFAULT_CORPUS_YEARS = (2003, 2004, 2005, 2006, 2007)

# Number of top frequent terms to remove as stop words
DEFAULT_STOP_WORDS_TOP_N = 9

# Number of results to return by default
DEFAULT_TOP_K = 20

# Number of queries in the evaluation set
NUM_QUERIES = 50


def get_corpus_paths(base_dir: Path) -> list[Path]:
    """Return list of corpus directory paths for each year."""
    return [base_dir / f"200{i}" for i in range(3, 8)]
