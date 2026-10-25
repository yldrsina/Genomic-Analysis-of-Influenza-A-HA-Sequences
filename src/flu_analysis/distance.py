from __future__ import annotations


def p_distance(first: str, second: str) -> float:
    comparable = differences = 0
    for a, b in zip(first, second):
        if a == "-" or b == "-":
            continue
        comparable += 1
        differences += a != b
    if not comparable:
        raise ValueError("sequences have no comparable ungapped positions")
    return differences / comparable


def distance_matrix(names: list[str], sequences: list[str]) -> dict[str, dict[str, float]]:
    if len(names) != len(sequences):
        raise ValueError("names and sequences must have equal lengths")
    matrix = {name: {other: 0.0 for other in names} for name in names}
    for i, name in enumerate(names):
        for j in range(i):
            value = p_distance(sequences[i], sequences[j])
            matrix[name][names[j]] = value
            matrix[names[j]][name] = value
    return matrix

