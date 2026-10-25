# Comparative Genomic Analysis of Influenza A HA Sequences

This project compares influenza A hemagglutinin (HA) nucleotide sequences, aligns
them, calculates pairwise genetic distances, builds a UPGMA phylogenetic tree,
and tests whether tree clusters are associated with subtype, sampling year, or
geographic origin.

The implementation uses only the Python standard library, so it can be run on a
fresh Python installation without a bioinformatics package stack. The included
dataset is a small, clearly labelled demonstration fixture. For a research
analysis, download complete HA records from NCBI using the included accession
manifest and rerun the same pipeline.

## Project structure

```text
data/
  sample_ha.fasta       # Offline demonstration sequences
  sample_metadata.csv   # Sequence metadata
  ncbi_accessions.csv   # Public NCBI accession manifest
src/flu_analysis/
  cli.py                # Command-line workflow
  fasta.py              # FASTA and metadata input
  alignment.py          # Needleman-Wunsch global alignment
  distance.py           # p-distance matrix
  tree.py               # UPGMA clustering and Newick export
  report.py             # TSV, JSON, and HTML report writers
scripts/
  download_ncbi.py      # NCBI EFetch downloader
tests/
  test_pipeline.py
```

## Quick start

From the project directory:

```powershell
python -m flu_analysis.cli `
  --fasta data\sample_ha.fasta `
  --metadata data\sample_metadata.csv `
  --outdir results
```

The command writes:

- `aligned.fasta`: globally aligned sequences
- `distance_matrix.tsv`: pairwise p-distances
- `tree.newick`: UPGMA tree
- `clusters.csv`: internal tree-cluster assignments
- `report.json`: machine-readable summary and metadata association statistics
- `report.html`: a readable results report

The package is run directly from a checkout with:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -v
```

## Downloading public sequences

The manifest contains accession IDs and metadata fields needed for the analysis.
Download records from NCBI's EFetch endpoint:

```powershell
python scripts\download_ncbi.py `
  --manifest data\ncbi_accessions.csv `
  --output data\ncbi_ha.fasta
```

The downloader requests nucleotide FASTA records from NCBI, checks that every
manifest accession was returned, and writes an audit JSON file beside the FASTA.
Always inspect the returned records and confirm that each record is the HA gene
(segment 4) before using results in a report. NCBI requests should be made
responsibly and are subject to NCBI usage policies.

Then run:

```powershell
python -m flu_analysis.cli `
  --fasta data\ncbi_ha.fasta `
  --metadata data\ncbi_accessions.csv `
  --outdir results\ncbi
```

## Methods

1. FASTA records are normalized to uppercase DNA and validated.
2. Sequences are globally aligned with Needleman-Wunsch using match `+1`,
   mismatch `-1`, and gap `-2`.
3. Pairwise p-distance is the number of mismatched aligned, non-gap nucleotide
   columns divided by the number of comparable columns.
4. A UPGMA tree is built from the p-distance matrix. UPGMA assumes a molecular
   clock; for publication-grade inference, compare this result with a
   maximum-likelihood method such as IQ-TREE or RAxML.
5. Metadata association is summarized using tree cut clusters and normalized
   mutual information (NMI). NMI is descriptive, not a hypothesis test.

## Reproducibility and interpretation

The output records the input files, alignment settings, sequence count, and
analysis date. The demonstration sequences are intentionally short and are not
appropriate for biological conclusions. Replace them with verified, homologous
HA records of comparable region and orientation, document accession versions,
and report sequence quality-control decisions before interpreting clustering by
year, subtype, or location.

