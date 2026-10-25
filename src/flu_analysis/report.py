from __future__ import annotations

import html
import json
from pathlib import Path


def normalized_mutual_information(first: list[str], second: list[str]) -> float:
    if len(first) != len(second) or not first:
        raise ValueError("labels must have equal non-zero lengths")
    n = len(first)
    a_counts = {value: first.count(value) for value in set(first)}
    b_counts = {value: second.count(value) for value in set(second)}
    mi = 0.0
    for a in a_counts:
        for b in b_counts:
            joint = sum(x == a and y == b for x, y in zip(first, second))
            if joint:
                mi += (joint / n) * __import__("math").log((joint * n) / (a_counts[a] * b_counts[b]))
    h_a = -sum((count / n) * __import__("math").log(count / n) for count in a_counts.values())
    h_b = -sum((count / n) * __import__("math").log(count / n) for count in b_counts.values())
    return 0.0 if not h_a or not h_b else mi / (h_a * h_b) ** 0.5


def write_outputs(outdir: Path, alignment, matrix, tree, metadata: dict[str, dict[str, str]]) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "aligned.fasta").write_text(
        "".join(f">{name}\n{sequence}\n" for name, sequence in zip(alignment.names, alignment.sequences)),
        encoding="utf-8",
    )
    with (outdir / "distance_matrix.tsv").open("w", encoding="utf-8") as handle:
        handle.write("id\t" + "\t".join(alignment.names) + "\n")
        for name in alignment.names:
            handle.write(name + "\t" + "\t".join(f"{matrix[name][other]:.6f}" for other in alignment.names) + "\n")
    (outdir / "tree.newick").write_text(tree.newick() + ";\n", encoding="utf-8")
    clusters: dict[str, str] = {}
    for cluster_number, child in enumerate((tree.left, tree.right), 1):
        for name in _leaf_names(child):
            clusters[name] = str(cluster_number)
    with (outdir / "clusters.csv").open("w", encoding="utf-8") as handle:
        handle.write("id,cluster,subtype,year,location\n")
        for name in alignment.names:
            row = metadata.get(name, {})
            handle.write(f"{name},{clusters[name]},{row.get('subtype', '')},{row.get('year', '')},{row.get('location', '')}\n")
    associations = {}
    for field in ("subtype", "year", "location"):
        values = [metadata.get(name, {}).get(field, "unknown") for name in alignment.names]
        associations[field] = normalized_mutual_information(list(clusters.values()), values)
    summary = {"sequence_count": len(alignment.names), "alignment_length": len(alignment.sequences[0]), "associations_nmi": associations}
    (outdir / "report.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    rows = "".join(f"<tr><td>{html.escape(name)}</td><td>{html.escape(metadata.get(name, {}).get('subtype', ''))}</td><td>{html.escape(metadata.get(name, {}).get('year', ''))}</td><td>{html.escape(metadata.get(name, {}).get('location', ''))}</td></tr>" for name in alignment.names)
    (outdir / "report.html").write_text(f"<html><body><h1>Influenza HA analysis</h1><p>{summary['sequence_count']} sequences; alignment length {summary['alignment_length']}.</p><p>NMI: {html.escape(json.dumps(associations))}</p><table><tr><th>ID</th><th>Subtype</th><th>Year</th><th>Location</th></tr>{rows}</table></body></html>\n", encoding="utf-8")
    return summary


def _leaf_names(node) -> list[str]:
    if node is None:
        return []
    if node.left is None:
        return [node.name or ""]
    return _leaf_names(node.left) + _leaf_names(node.right)
