"""Evaluation: load relevance judgements, compute precision, recall, F1, MAP."""

from pathlib import Path
from typing import Any

from ir.config import DEFAULT_JUDGEMENTS_PATH, NUM_QUERIES


def load_judgements(path: Path | str = DEFAULT_JUDGEMENTS_PATH) -> list[list[str]]:
    """
    Load judgements file: one line per judgement, format 'query_num doc_id'.
    Returns list of 50 lists; query_docs[i] = list of relevant doc ids (with .ham).
    """
    path = Path(path)
    query_docs: list[list[str]] = [[] for _ in range(NUM_QUERIES)]
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            i = line.find(" ")
            if i <= 0:
                continue
            num = int(line[:i])
            doc_id = line[i + 1 :].strip()
            if not doc_id.endswith(".ham"):
                doc_id += ".ham"
            if 1 <= num <= NUM_QUERIES:
                query_docs[num - 1].append(doc_id)
    return query_docs


def _precision_recall_at_cutoffs(
    scores: list[tuple[str, float]],
    relevant: set[str],
) -> tuple[list[float], list[float], list[int]]:
    """Compute precision and recall at each rank; return precisions, recalls, positions of relevant docs."""
    precision = []
    recall = []
    r_positions: list[int] = []
    tp = 0
    retrieved = 0
    n_relevant = len(relevant)
    for doc_id, _ in scores:
        retrieved += 1
        if doc_id in relevant:
            tp += 1
            r_positions.append(retrieved - 1)
        precision.append(tp / retrieved)
        recall.append(tp / n_relevant if n_relevant else 0.0)
    return precision, recall, r_positions


def f_measure(precision: float, recall: float, beta: float = 1.0) -> float:
    """F_beta measure. beta=1 gives F1."""
    if precision + recall == 0:
        return 0.0
    return ((beta * beta + 1) * precision * recall) / (beta * beta * precision + recall)


def average_precision(precision_at_ranks: list[float]) -> float:
    """Mean of precision at each relevant document (AP)."""
    if not precision_at_ranks:
        return 0.0
    return sum(precision_at_ranks) / len(precision_at_ranks)


def evaluate_ranking(
    scores: list[tuple[str, float]],
    relevant_doc_ids: list[str],
    k: int | None = None,
) -> dict[str, Any]:
    """
    Compute precision, recall, F1, and MAP for a single query.
    If k is given, only consider top-k retrieved for final P/R (interpolation at k).
    """
    relevant = set(relevant_doc_ids)
    if not relevant:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "map": 0.0}
    precision_list, recall_list, r_positions = _precision_recall_at_cutoffs(scores, relevant)
    if not precision_list:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "map": 0.0}
    idx = (k - 1) if k and k <= len(precision_list) else (len(precision_list) - 1)
    p = precision_list[idx]
    r = recall_list[idx]
    prec_at_rel = [precision_list[i] for i in r_positions]
    return {
        "precision": p,
        "recall": r,
        "f1": f_measure(p, r, beta=1.0),
        "map": average_precision(prec_at_rel),
    }
