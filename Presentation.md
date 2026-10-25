# Comparative Genomic Analysis and Phylogenetic Tree Construction of Influenza A Strains

> **Presentation-ready slide script**
>
> This document is organized as slides. Each slide contains suggested on-slide
> content followed by speaker notes. The current results are from four public
> NCBI HA records and should be presented as a pilot/demo analysis, not as a
> definitive evolutionary study.

---

## Slide 1 — Title

### Comparative Genomic Analysis and Phylogenetic Tree Construction of Influenza A Strains

**Subtitle:**  
Using hemagglutinin (HA) nucleotide sequences to compare genetic similarity and evolutionary relationships

**Presented by:** `[Your name]`  
**Course / department:** `[Course or department]`  
**Date:** `[Presentation date]`

### Speaker notes

This project demonstrates a complete bioinformatics workflow for studying
influenza virus evolution. We collected HA gene sequences from a public
database, aligned them, measured their genetic differences, constructed a
phylogenetic tree, and compared the resulting clusters with subtype, year, and
geographic origin.

---

## Slide 2 — Background: Influenza A

- Influenza A is an RNA virus that infects humans, birds, and other animals.
- Its genome contains multiple gene segments.
- Two important surface proteins are:
  - **Hemagglutinin (HA):** helps the virus attach to host cells.
  - **Neuraminidase (NA):** helps newly formed virus particles leave infected cells.
- Influenza A subtypes are commonly written as combinations such as:
  - **H1N1**
  - **H3N2**

### Speaker notes

The HA gene is useful for comparative genomics because it changes over time.
Comparing HA sequences can reveal how similar or different viral strains are.
This project focuses on HA rather than analyzing the complete influenza genome.

---

## Slide 3 — Research question

### Main question

> How genetically similar are selected influenza A HA sequences, and do they
> cluster according to subtype, sampling year, or geographic origin?

### Specific objectives

1. Obtain public influenza HA sequences.
2. Associate each sequence with metadata:
   - subtype,
   - sampling year,
   - location.
3. Align the nucleotide sequences.
4. Calculate pairwise genetic distances.
5. Build a phylogenetic tree.
6. Compare tree clusters with the metadata.

### Speaker notes

The project is not only about producing a tree. It also asks whether the groups
in the tree correspond to biological or epidemiological labels.

---

## Slide 4 — Overall workflow

```text
Public NCBI records
        ↓
FASTA sequences + metadata
        ↓
Sequence validation
        ↓
Global sequence alignment
        ↓
Pairwise p-distance matrix
        ↓
UPGMA phylogenetic tree
        ↓
Cluster and metadata comparison
        ↓
Report and interpretation
```

### Speaker notes

Each step produces an input for the next step. This makes the analysis
reproducible and allows us to inspect intermediate results instead of treating
the tree as a black box.

---

## Slide 5 — Dataset

### Four public HA records were analyzed

| Identifier | Accession | Subtype | Year | Location |
|---|---|---|---:|---|
| A_Puerto_Rico_8_1934_HA | CY009397.1 | H1N1 | 1934 | United States |
| A_California_04_2009_HA | CY121680.1 | H1N1 | 2009 | United States |
| A_Hong_Kong_1_1968_HA | CY032012.1 | H3N2 | 1968 | Hong Kong |
| A_Hong_Kong_4801_2014_HA | CY163680.1 | H3N2 | 2014 | Hong Kong |

### Dataset summary

- Number of sequences: **4**
- Gene analyzed: **HA**
- Source: **NCBI nucleotide database**
- Sequence input: [`data/ncbi_ha.fasta`](data/ncbi_ha.fasta)
- Metadata input: [`data/ncbi_accessions.csv`](data/ncbi_accessions.csv)

### Speaker notes

This is a deliberately small dataset. It is sufficient to demonstrate the
workflow, but it is not large or balanced enough to support broad conclusions
about all H1N1, H3N2, years, or locations.

---

## Slide 6 — FASTA sequence format

Example FASTA record:

```text
>A_California_04_2009_HA accession=CY121680.1
GGAAAACAAAAGCAACAAAAATGAAGGCAATACTAGTAGTTCTGCTATATAC...
```

### FASTA components

- The line beginning with `>` is the sequence identifier.
- The following line or lines contain nucleotide characters.
- Valid nucleotide characters include:
  - `A`, `C`, `G`, `T`
  - `N` for an unknown base
  - `-` for an alignment gap

### Input validation

The project checks that:

- every sequence has an identifier,
- sequences are not empty,
- identifiers are unique,
- nucleotide characters are valid,
- every FASTA identifier has corresponding metadata.

### Speaker notes

Input validation is important because incorrect or mismatched sequence data can
produce misleading distances and trees.

---

## Slide 7 — Sequence alignment

### Why align sequences?

Sequences can contain insertions or deletions. Alignment places comparable
nucleotides in the same columns.

Example:

```text
Sequence 1: A C G T
Sequence 2: A - G T
```

### Method used

- Global Needleman–Wunsch alignment
- Match score: `+1`
- Mismatch score: `-1`
- Gap score: `-2`
- Progressive alignment for multiple sequences

### Result

- Final alignment length: **1,739 positions**
- Output: [`results/ncbi/aligned.fasta`](results/ncbi/aligned.fasta)

### Speaker notes

The alignment gives the analysis a common coordinate system. Once sequences are
aligned, the nucleotide in column 100 of one sequence can be compared with the
nucleotide in column 100 of another sequence.

For a publication-quality analysis, a specialized aligner such as MAFFT or
MUSCLE should be compared with this educational implementation.

---

## Slide 8 — Genetic distance calculation

### p-distance

The project calculates:

```text
p-distance =
number of different comparable positions
---------------------------------------
number of comparable positions
```

- Identical positions contribute no difference.
- Mismatched nucleotide positions contribute one difference.
- Columns containing a gap are excluded.
- A distance of `0.0` means identical at the compared positions.

### Output

- Pairwise distance matrix:
  [`results/ncbi/distance_matrix.tsv`](results/ncbi/distance_matrix.tsv)

### Speaker notes

The p-distance is a simple proportion of observed differences. It does not
correct for multiple substitutions at the same position, so more advanced
phylogenetic models may be appropriate for larger or more divergent datasets.

---

## Slide 9 — Pairwise distance results

### Selected p-distances

| Sequence pair | p-distance | Interpretation |
|---|---:|---|
| H1N1 1934 vs H1N1 2009 | 0.180361 | About 18.0% of comparable positions differ |
| H3N2 1968 vs H3N2 2014 | 0.739084 | About 73.9% of comparable positions differ |
| H1N1 1934 vs H3N2 1968 | 0.754202 | About 75.4% differ |
| H1N1 2009 vs H3N2 1968 | 0.737515 | About 73.8% differ |

### Initial observation

- The H1N1 pair is closer to each other than to the H3N2 records.
- H1N1 and H3N2 are strongly separated in this dataset.
- The H3N2 pair has an unexpectedly high distance and requires quality control.

### Speaker notes

The distance matrix suggests a subtype-based split. However, the H3N2 value of
approximately 0.739 is unusually high for two records with the same subtype.
Before treating that value as a biological discovery, we should verify sequence
coverage, orientation, record annotation, and alignment quality.

---

## Slide 10 — Phylogenetic method: UPGMA

### UPGMA

UPGMA means **Unweighted Pair Group Method with Arithmetic Mean**.

The algorithm:

1. Finds the two closest sequences or groups.
2. Joins them into a cluster.
3. Calculates average distances to the remaining groups.
4. Repeats until all sequences are connected.

### Assumption

UPGMA assumes approximately equal evolutionary rates across lineages, also
called a molecular clock assumption.

### Output

- Newick tree:
  [`results/ncbi/tree.newick`](results/ncbi/tree.newick)

### Speaker notes

UPGMA is simple and useful for demonstrating the workflow. It is not necessarily
the best method for real influenza evolutionary inference because viral
lineages may evolve at different rates.

---

## Slide 11 — Phylogenetic tree result

### Simplified tree

```text
                 ┌── A_California_04_2009_HA
             ┌───┤
             │   └── A_Puerto_Rico_8_1934_HA
─────────────┤
             │   ┌── A_Hong_Kong_1_1968_HA
             └───┤
                 └── A_Hong_Kong_4801_2014_HA
```

### Interpretation

- The two H1N1 sequences form one main group.
- The two H3N2 sequences form another main group.
- The two subtype groups are separated by a large distance.

### Speaker notes

The tree represents inferred similarity based on the alignment and distance
matrix. It does not prove direct ancestry. For example, the 2009 H1N1 virus
should not be described as directly descending from the 1934 record based only
on this tree.

---

## Slide 12 — Tree clusters and metadata

### Cluster assignments

| Sequence | Tree cluster | Subtype | Year | Location |
|---|---:|---|---:|---|
| A_Puerto_Rico_8_1934_HA | 1 | H1N1 | 1934 | United States |
| A_California_04_2009_HA | 1 | H1N1 | 2009 | United States |
| A_Hong_Kong_1_1968_HA | 2 | H3N2 | 1968 | Hong Kong |
| A_Hong_Kong_4801_2014_HA | 2 | H3N2 | 2014 | Hong Kong |

### Main observation

```text
Cluster 1 = H1N1 = United States records
Cluster 2 = H3N2 = Hong Kong records
```

### Output

- [`results/ncbi/clusters.csv`](results/ncbi/clusters.csv)

### Speaker notes

The subtype pattern is clear in this dataset. The location pattern looks clear
too, but subtype and location are confounded: every United States sample is H1N1
and every Hong Kong sample is H3N2. Therefore, this dataset cannot tell us
whether subtype, geography, or both explain the clustering.

---

## Slide 13 — Metadata association results

### Normalized Mutual Information (NMI)

| Metadata variable | NMI | Meaning in this dataset |
|---|---:|---|
| Subtype | 1.0000 | Perfect agreement with tree clusters |
| Location | 1.0000 | Perfect agreement with tree clusters |
| Sampling year | 0.7071 | Partial agreement with tree clusters |

### How to read NMI

- `0` means little or no agreement.
- `1` means perfect agreement.
- NMI is descriptive here; it is not a hypothesis test.

### Output

- [`results/ncbi/report.json`](results/ncbi/report.json)
- [`results/ncbi/report.html`](results/ncbi/report.html)

### Speaker notes

Subtype and location both have an NMI of 1.0 because the same two groups are
being represented by both labels. The year score is lower because each cluster
contains one older and one newer sample:

```text
Cluster 1: 1934 and 2009
Cluster 2: 1968 and 2014
```

---

## Slide 14 — Main findings

1. The workflow successfully processed four public HA sequences.
2. The sequences were aligned to 1,739 positions.
3. The UPGMA tree produced two main groups.
4. The groups corresponded to:
   - H1N1 versus H3N2,
   - and, in this dataset, United States versus Hong Kong.
5. Sampling year showed a weaker pattern.
6. The H3N2 pair showed a very high calculated p-distance and needs verification.

### Short result statement

> In this pilot dataset, HA sequences clustered primarily by influenza subtype,
> with H1N1 records in one group and H3N2 records in another. Because subtype
> and location were completely confounded, the effect of geography cannot be
> separated from the effect of subtype.

---

## Slide 15 — Limitations

### Dataset limitations

- Only four sequences were analyzed.
- Only two subtypes were included.
- The geographic sampling was not balanced.
- The number of sequences is too small for broad evolutionary conclusions.
- Sampling years and locations are not independently represented.

### Method limitations

- Progressive alignment is a simplified educational method.
- p-distance does not model repeated substitutions.
- UPGMA assumes equal evolutionary rates.
- No bootstrap support values were calculated.
- No formal statistical test of metadata association was performed.

### Data-quality concern

- The H3N2 pair has a p-distance of `0.739084`.
- Sequence region, orientation, annotation, and alignment quality should be
  checked before interpreting this value biologically.

### Speaker notes

These limitations do not mean the workflow failed. They define what the current
results can responsibly claim. The project is a reproducible pilot analysis and
an educational demonstration of the process.

---

## Slide 16 — Improvements for a stronger study

### Data improvements

- Include many more sequences.
- Sample each subtype from multiple countries.
- Include multiple years for each subtype and location.
- Use complete, homologous HA sequences.
- Record accession versions and collection dates.

### Analysis improvements

- Use MAFFT or MUSCLE for multiple-sequence alignment.
- Compare UPGMA with maximum-likelihood methods such as IQ-TREE or RAxML.
- Use an appropriate nucleotide substitution model.
- Calculate bootstrap support.
- Add quality-control filtering.
- Test metadata associations statistically.

### Visualization improvements

- Draw the tree with colored subtype labels.
- Add year and location annotations.
- Display branch support values.
- Plot pairwise distances as a heatmap.

---

## Slide 17 — Reproducibility

### Run the analysis

From the project directory:

```powershell
$env:PYTHONPATH = "$PWD\src"

python -m flu_analysis.cli `
  --fasta data\ncbi_ha.fasta `
  --metadata data\ncbi_accessions.csv `
  --outdir results\ncbi
```

### Run tests

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m unittest discover -s tests -v
```

### Main project files

- Workflow entry point: [`src/flu_analysis/cli.py`](src/flu_analysis/cli.py)
- FASTA and metadata input: [`src/flu_analysis/fasta.py`](src/flu_analysis/fasta.py)
- Alignment: [`src/flu_analysis/alignment.py`](src/flu_analysis/alignment.py)
- Distances: [`src/flu_analysis/distance.py`](src/flu_analysis/distance.py)
- Tree: [`src/flu_analysis/tree.py`](src/flu_analysis/tree.py)
- Reports: [`src/flu_analysis/report.py`](src/flu_analysis/report.py)

### Speaker notes

The project uses Python's standard library and keeps each analysis step in a
separate module. This makes the work easier to understand, test, and reproduce.

---

## Slide 18 — Conclusion

### Conclusions

- HA sequences can be used to compare influenza virus strains.
- Alignment creates comparable nucleotide positions.
- Genetic distances quantify sequence differences.
- A phylogenetic tree summarizes relationships among strains.
- In this four-sequence pilot:
  - H1N1 sequences clustered together.
  - H3N2 sequences clustered together.
  - The apparent location association is confounded with subtype.
  - Year was less clearly associated with clustering.
- Larger, balanced datasets and more advanced phylogenetic methods are required
  for strong evolutionary conclusions.

### Final message

> Bioinformatics connects public sequence data, computational analysis, and
> biological interpretation to help us study viral evolution and genetic
> diversity.

---

## Slide 19 — Questions

### Thank you

**Questions?**

### Suggested discussion questions

1. Why is HA a useful gene for influenza comparison?
2. Why is sequence alignment necessary before calculating distances?
3. What does a branch in a phylogenetic tree represent?
4. Why can we not separate subtype and location effects in this dataset?
5. What additional sequences would improve the study?

---

## Appendix A — Technical method summary

| Step | Implementation in this project |
|---|---|
| Sequence input | FASTA parser with validation |
| Metadata input | CSV keyed by sequence ID |
| Alignment | Needleman–Wunsch global alignment |
| Match score | `+1` |
| Mismatch score | `-1` |
| Gap score | `-2` |
| Genetic distance | p-distance |
| Gap handling | Gap-containing columns excluded |
| Tree method | UPGMA |
| Tree format | Newick |
| Metadata comparison | Two root clusters and NMI |
| Report formats | HTML, JSON, TSV, FASTA, Newick |

---

## Appendix B — Exact Newick output

```text
((A_California_04_2009_HA:0.090180,A_Puerto_Rico_8_1934_HA:0.090180):0.288409,(A_Hong_Kong_1_1968_HA:0.369542,A_Hong_Kong_4801_2014_HA:0.369542):0.009048);
```

---

## Appendix C — Suggested figure list

Use these figures or tables when converting this Markdown into slides:

1. **Workflow diagram:** Slide 4.
2. **Dataset table:** Slide 5.
3. **Alignment excerpt:** Slide 7.
4. **Distance heatmap:** Create from `distance_matrix.tsv`.
5. **Phylogenetic tree:** Render `tree.newick` using FigTree, iTOL, or another
   Newick-compatible viewer.
6. **Cluster metadata table:** Slide 12.
7. **NMI bar chart:** Plot subtype `1.0`, location `1.0`, and year `0.7071`.

### Recommended visual color scheme

- H1N1: blue
- H3N2: orange
- United States: blue-gray
- Hong Kong: red-orange
- Older samples: lighter shade
- Newer samples: darker shade

