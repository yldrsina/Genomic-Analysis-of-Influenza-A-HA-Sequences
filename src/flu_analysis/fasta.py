from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SequenceRecord:
    name: str
    sequence: str


def read_fasta(path: Path) -> list[SequenceRecord]:
    records: list[SequenceRecord] = []
    name: str | None = None
    chunks: list[str] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if name is not None:
                records.append(_make_record(name, chunks, path, line_number))
            name = line[1:].split()[0]
            if not name:
                raise ValueError(f"{path}:{line_number}: empty FASTA identifier")
            chunks = []
        elif name is None:
            raise ValueError(f"{path}:{line_number}: sequence data precedes a FASTA header")
        else:
            chunks.append(line)
    if name is not None:
        records.append(_make_record(name, chunks, path, len(path.read_text(encoding="utf-8").splitlines()) + 1))
    if not records:
        raise ValueError(f"{path}: no FASTA records found")
    if len({record.name for record in records}) != len(records):
        raise ValueError(f"{path}: FASTA identifiers must be unique")
    return records


def _make_record(name: str, chunks: list[str], path: Path, line_number: int) -> SequenceRecord:
    sequence = "".join(chunks).upper().replace("U", "T")
    if not sequence:
        raise ValueError(f"{path}:{line_number}: empty sequence for {name}")
    invalid = set(sequence) - set("ACGTN-")
    if invalid:
        raise ValueError(f"{path}:{line_number}: invalid bases for {name}: {sorted(invalid)}")
    return SequenceRecord(name, sequence)


def read_metadata(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not rows[0].get("id"):
        raise ValueError(f"{path}: metadata must contain an id column and at least one row")
    result = {row["id"]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"{path}: metadata ids must be unique")
    return result

