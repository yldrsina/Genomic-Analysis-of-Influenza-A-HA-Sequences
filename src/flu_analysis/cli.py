from __future__ import annotations

import argparse
from pathlib import Path

from .alignment import progressive_align
from .distance import distance_matrix
from .fasta import read_fasta, read_metadata
from .report import write_outputs
from .tree import upgma


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze influenza HA sequences")
    parser.add_argument("--fasta", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()
    records = read_fasta(args.fasta)
    metadata = read_metadata(args.metadata)
    missing = [record.name for record in records if record.name not in metadata]
    if missing:
        raise SystemExit(f"metadata is missing FASTA ids: {', '.join(missing)}")
    alignment = progressive_align([(record.name, record.sequence) for record in records])
    matrix = distance_matrix(alignment.names, alignment.sequences)
    summary = write_outputs(args.outdir, alignment, matrix, upgma(matrix), metadata)
    print(f"Analyzed {summary['sequence_count']} sequences; outputs written to {args.outdir}")


if __name__ == "__main__":
    main()

