import tempfile
import unittest
from pathlib import Path

from flu_analysis.alignment import needleman_wunsch
from flu_analysis.distance import p_distance
from flu_analysis.fasta import read_fasta
from flu_analysis.cli import main


class PipelineTests(unittest.TestCase):
    def test_global_alignment_preserves_bases(self):
        first, second = needleman_wunsch("ACGT", "AGT")
        self.assertEqual(len(first), len(second))
        self.assertEqual(first.replace("-", ""), "ACGT")
        self.assertEqual(second.replace("-", ""), "AGT")

    def test_distance_ignores_gap_columns(self):
        self.assertAlmostEqual(p_distance("A-C", "ATC"), 0.0)
        self.assertAlmostEqual(p_distance("AAC", "ATC"), 1 / 3)

    def test_demo_cli_writes_outputs(self):
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as directory:
            import sys
            sys.argv = ["flu-analysis", "--fasta", str(root / "data/sample_ha.fasta"), "--metadata", str(root / "data/sample_metadata.csv"), "--outdir", directory]
            main()
            self.assertTrue((Path(directory) / "tree.newick").read_text().strip().endswith(";"))
            self.assertTrue((Path(directory) / "report.json").exists())


if __name__ == "__main__":
    unittest.main()
