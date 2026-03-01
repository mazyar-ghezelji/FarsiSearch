"""Command-line interface for indexing, search, and evaluation."""

from __future__ import unicode_literals

import argparse
from pathlib import Path

from ir import __version__
from ir.config import (
    DEFAULT_INDEX_PATH,
    DEFAULT_JUDGEMENTS_PATH,
    DEFAULT_QUERIES_DIR,
    DEFAULT_TOP_K,
    NUM_QUERIES,
)
from ir.index import InvertedIndex
from ir.preprocess import PersianPreprocessor
from ir.query import process_query_tokens
from ir.scoring import score_documents, SCORE_LNN_LTN, SCORE_LNC_LTC
from ir.evaluation import load_judgements, evaluate_ranking


def cmd_index(args: argparse.Namespace) -> None:
    corpus = Path(args.corpus)
    index = InvertedIndex()
    index.build_from_corpus(corpus_dir=corpus, remove_stop_words=True)
    out = Path(args.output)
    index.save(out)
    print(f"Indexed {index.docs_count} documents → {out}")


def cmd_search(args: argparse.Namespace) -> None:
    index = InvertedIndex()
    index.load(Path(args.index))
    preprocessor = PersianPreprocessor()
    terms, full = process_query_tokens(args.query, preprocessor, index.dictionary)
    mode = SCORE_LNC_LTC if args.cosine else SCORE_LNN_LTN
    scores = score_documents(
        index.dictionary,
        index.docs_size,
        index.docs_count,
        terms,
        full,
        mode=mode,
    )
    k = min(args.top_k, len(scores))
    for i, (doc_id, score) in enumerate(scores[:k], 1):
        print(f"{i}. {doc_id}  {score:.4f}")


def cmd_evaluate(args: argparse.Namespace) -> None:
    index = InvertedIndex()
    index.load(Path(args.index))
    preprocessor = PersianPreprocessor()
    query_docs = load_judgements(Path(args.judgements))
    mode = SCORE_LNC_LTC if args.cosine else SCORE_LNN_LTN
    total_map = 0.0
    total_f1 = 0.0
    queries_dir = Path(args.queries)
    for qid in range(1, NUM_QUERIES + 1):
        qpath = queries_dir / f"{qid}.q"
        if not qpath.exists():
            continue
        with open(qpath, "r", encoding="utf-8") as f:
            query = f.read()
        terms, full = process_query_tokens(query, preprocessor, index.dictionary)
        scores = score_documents(
            index.dictionary,
            index.docs_size,
            index.docs_count,
            terms,
            full,
            mode=mode,
        )
        rel = query_docs[qid - 1]
        metrics = evaluate_ranking(scores, rel)
        total_map += metrics["map"]
        total_f1 += metrics["f1"]
    n = NUM_QUERIES
    print(f"Total MAP:  {total_map / n:.4f}")
    print(f"Total F1:  {total_f1 / n:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ir",
        description="Information Retrieval system for the Hamshahri corpus (Persian).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index", help="Build index from corpus")
    p_index.add_argument(
        "--corpus",
        type=str,
        default="Documents/HamshahriData/HamshahriCorpus",
        help="Corpus root",
    )
    p_index.add_argument("--output", type=str, default=str(DEFAULT_INDEX_PATH), help="Output index path")
    p_index.set_defaults(func=cmd_index)

    p_search = sub.add_parser("search", help="Run a query")
    p_search.add_argument("query", type=str, help="Query text (Persian)")
    p_search.add_argument("--index", type=str, default=str(DEFAULT_INDEX_PATH), help="Index path")
    p_search.add_argument("--top-k", type=int, default=DEFAULT_TOP_K, help="Number of results")
    p_search.add_argument("--cosine", action="store_true", help="Use lnc.ltc (cosine) scoring")
    p_search.set_defaults(func=cmd_search)

    p_eval = sub.add_parser("evaluate", help="Evaluate on full query set")
    p_eval.add_argument("--index", type=str, default=str(DEFAULT_INDEX_PATH), help="Index path")
    p_eval.add_argument("--queries", type=str, default=str(DEFAULT_QUERIES_DIR), help="Queries directory")
    p_eval.add_argument("--judgements", type=str, default=str(DEFAULT_JUDGEMENTS_PATH), help="Judgements file")
    p_eval.add_argument("--cosine", action="store_true", help="Use lnc.ltc scoring")
    p_eval.set_defaults(func=cmd_evaluate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
