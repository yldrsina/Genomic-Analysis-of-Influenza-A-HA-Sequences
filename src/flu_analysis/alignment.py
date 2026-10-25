from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Alignment:
    names: list[str]
    sequences: list[str]


def needleman_wunsch(first: str, second: str, match: int = 1, mismatch: int = -1, gap: int = -2) -> tuple[str, str]:
    rows, columns = len(first) + 1, len(second) + 1
    score = [[0] * columns for _ in range(rows)]
    trace = [[""] * columns for _ in range(rows)]
    for i in range(1, rows):
        score[i][0] = i * gap
        trace[i][0] = "U"
    for j in range(1, columns):
        score[0][j] = j * gap
        trace[0][j] = "L"
    for i in range(1, rows):
        for j in range(1, columns):
            diagonal = score[i - 1][j - 1] + (match if first[i - 1] == second[j - 1] else mismatch)
            up = score[i - 1][j] + gap
            left = score[i][j - 1] + gap
            best = max(diagonal, up, left)
            score[i][j] = best
            trace[i][j] = "D" if best == diagonal else ("U" if best == up else "L")
    aligned_first, aligned_second = [], []
    i, j = len(first), len(second)
    while i or j:
        direction = trace[i][j]
        if direction == "D":
            aligned_first.append(first[i - 1])
            aligned_second.append(second[j - 1])
            i, j = i - 1, j - 1
        elif direction == "U":
            aligned_first.append(first[i - 1])
            aligned_second.append("-")
            i -= 1
        else:
            aligned_first.append("-")
            aligned_second.append(second[j - 1])
            j -= 1
    return "".join(reversed(aligned_first)), "".join(reversed(aligned_second))


def progressive_align(records: list[tuple[str, str]]) -> Alignment:
    if not records:
        raise ValueError("at least one sequence is required")
    reference_name, reference = records[0]
    aligned_reference = reference
    aligned = [reference]
    for _, sequence in records[1:]:
        new_reference, new_sequence = needleman_wunsch(reference, sequence)
        if len(new_reference) != len(aligned_reference):
            remapped: list[str] = []
            for old in aligned:
                cursor = 0
                chars: list[str] = []
                for char in new_reference:
                    if char == "-":
                        chars.append("-")
                    else:
                        chars.append(old[cursor])
                        cursor += 1
                remapped.append("".join(chars))
            aligned = remapped
            aligned_reference = new_reference
        aligned.append(new_sequence)
        reference = new_reference.replace("-", "")
    return Alignment([reference_name] + [name for name, _ in records[1:]], aligned)

