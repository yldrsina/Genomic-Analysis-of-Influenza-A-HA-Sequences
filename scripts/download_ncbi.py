from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


def main() -> None:
    parser = argparse.ArgumentParser(description="Download manifest accessions from NCBI EFetch")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not all(row.get("accession") for row in rows):
        raise SystemExit("manifest must contain at least one accession per row")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    chunks: list[str] = []
    returned: set[str] = set()
    for row in rows:
        accession = row["accession"]
        query = urlencode({"db": "nuccore", "id": accession, "rettype": "fasta", "retmode": "text"})
        with urlopen(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{query}", timeout=30) as response:
            text = response.read().decode("utf-8")
        if not text.startswith(">"):
            raise SystemExit(f"NCBI returned no FASTA for {accession}")
        header = text.splitlines()[0]
        returned.add(header.split()[0].lstrip(">"))
        chunks.append(f">{row['id']} accession={accession}\n{''.join(text.splitlines()[1:])}\n")
        time.sleep(0.34)
    args.output.write_text("".join(chunks), encoding="utf-8")
    audit = {"manifest": str(args.manifest), "accessions_requested": [row["accession"] for row in rows], "records_returned": sorted(returned)}
    args.output.with_suffix(".audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(f"Downloaded {len(rows)} records to {args.output}")


if __name__ == "__main__":
    main()

