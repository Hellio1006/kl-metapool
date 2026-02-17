import unittest
import papermill as pm
import tempfile
from pathlib import Path
import os

# ==========================================
# 1. Configuration & Parameters
# ==========================================
NOTEBOOK = "tellseq_D_variable_volume_pooling.ipynb"
CURRENT_SET_ID = "col19to24"  # Change this ID for different test sets
EXPECTED_PICKLIST = f"Tellseq_iSeqnormpool_set_{CURRENT_SET_ID}.txt"

class TestTellseqD_Simple(unittest.TestCase):
    def setUp(self):
        """Set up standard paths"""
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.test_output_dir = os.path.join(self.base_dir, 'test_output')
        self.test_data_dir = os.path.join(self.base_dir, 'test_data')

    def test_variable_volume_pooling(self):
        """Execute notebook and verify picklist generation"""
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            
            # 2. Define Parameters for the Notebook
        
            test_values = {
                "plate_df_set_fp": os.path.join(self.test_output_dir, "QC", f"Tellseq_plate_df_C_set_{CURRENT_SET_ID}.txt"),
                "read_counts_fps": [os.path.join(self.test_data_dir, "Demux", "Tellseq_fastqc_sequence_counts.tsv")],
                "dynamic_range": 5,
                "iseqnormed_picklist_fbase": str(tmp_root / "Tellseq_iSeqnormpool")
            }
            
            # 3. Run Notebook
            pm.execute_notebook(
                input_path=os.path.join(self.base_dir, NOTEBOOK),
                output_path=str(tmp_root / "executed_test.ipynb"),
                parameters={"test_dict": test_values},
                log_output=True,
            )

            # 4. Verify Output File
            produced_file = tmp_root / EXPECTED_PICKLIST
            
            # Check if file exists
            self.assertTrue(produced_file.exists(), f"Missing output file: {EXPECTED_PICKLIST}")


if __name__ == "__main__":
    unittest.main()