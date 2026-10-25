from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    name: str | None
    left: "Node | None" = None
    right: "Node | None" = None
    height: float = 0.0
    size: int = 1

    def newick(self) -> str:
        if self.left is None:
            return _quote(self.name or "")
        left_length = max(0.0, self.height - self.left.height)
        right_length = max(0.0, self.height - (self.right.height if self.right else 0.0))
        return f"({self.left.newick()}:{left_length:.6f},{self.right.newick()}:{right_length:.6f})"


def upgma(matrix: dict[str, dict[str, float]]) -> Node:
    if not matrix:
        raise ValueError("distance matrix is empty")
    clusters = {name: Node(name=name) for name in matrix}
    distances = {(a, b): matrix[a][b] for a in matrix for b in matrix if a != b}
    while len(clusters) > 1:
        pair = min(((a, b) for a in clusters for b in clusters if a < b), key=lambda p: distances[p])
        a, b = pair
        left, right = clusters.pop(a), clusters.pop(b)
        merged_name = f"{a}|{b}"
        merged = Node(None, left, right, distances[pair] / 2, left.size + right.size)
        for other in clusters:
            distances[(merged_name, other)] = distances[(other, merged_name)] = (
                distances[(a, other)] * left.size + distances[(b, other)] * right.size
            ) / merged.size
        distances = {key: value for key, value in distances.items() if a not in key and b not in key}
        clusters[merged_name] = merged
    return next(iter(clusters.values()))


def _quote(name: str) -> str:
    return name.replace(" ", "_").replace(":", "_")
