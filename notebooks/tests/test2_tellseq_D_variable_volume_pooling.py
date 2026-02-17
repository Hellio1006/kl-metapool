import unittest
import papermill as pm
import tempfile
from pathlib import Path
import os
import glob

NOTEBOOK_NAME = "tellseq_D_variable_volume_pooling.ipynb"

class TestTellseqD(unittest.TestCase):
   
    def setUp(self):
        """Set up paths before starting tests"""
        self.test_file_path = os.path.abspath(__file__)
        self.notebooks_dir = os.path.dirname(os.path.dirname(self.test_file_path)) 
        self.test_output_dir = os.path.join(self.notebooks_dir, 'test_output')
        self.test_data_dir = os.path.join(self.notebooks_dir, 'test_data')

    def test_iseqnorm_picklist_dynamic(self):
        """Test Notebook D dynamically by extracting the ID from the input filename"""
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            

            search_pattern = os.path.join(self.test_output_dir, "QC", "Tellseq_plate_df_C_set_*.txt")
            matching_files = glob.glob(search_pattern)
            
            if not matching_files:
                self.fail(f"Could not find input file for testing: {search_pattern}")
            
         
            input_plate_c_fp = matching_files[0]
            
           
            filename = os.path.basename(input_plate_c_fp)
            extracted_id = filename.split('_set_')[-1].replace('.txt', '')
            
          
            test_values = {
                'plate_df_set_fp': input_plate_c_fp,
                'read_counts_fps': [
                    os.path.join(self.test_data_dir, "Demux", "Tellseq_fastqc_sequence_counts.tsv")
                ],
                'dynamic_range': 5,
                'iseqnormed_picklist_fbase': str(tmp_path / "Tellseq_iSeqnormpool")
            }

            # 5. Execute Notebook (Overwrites the top-level 'test_dict = None')
            pm.execute_notebook(
                input_path=os.path.join(self.notebooks_dir, NOTEBOOK_NAME),
                output_path=str(tmp_path / "executed_test_D.ipynb"),
                parameters={'test_dict': test_values},
                log_output=True,
            )

            # 6. Dynamically verify the output filename
            # Based on notebook logic: {{fbase}}_set_{{extracted_id}}.txt is generated
            expected_filename = f"Tellseq_iSeqnormpool_set_{extracted_id}.txt"
            produced_picklist_fp = tmp_path / expected_filename

            # Check if the file exists
            self.assertTrue(produced_picklist_fp.exists(),
                            msg=f"Notebook failed to produce the output file: {expected_filename}")

            # 7. Compare the actual result with the Golden File (expected value)
            golden_picklist_fp = os.path.join(self.test_output_dir, "Pooling", expected_filename)
            
            if os.path.exists(golden_picklist_fp):
                with open(produced_picklist_fp, 'r') as out, open(golden_picklist_fp, 'r') as gold:
                    out_lines = out.readlines()
                    gold_lines = gold.readlines()

                    # Compare line count and content
                    self.assertEqual(len(out_lines), len(gold_lines), 
                                     msg=f"Line count mismatch: {expected_filename}")
                    
                    for i, (o_line, g_line) in enumerate(zip(out_lines, gold_lines), 1):
                        self.assertEqual(o_line.strip(), g_line.strip(),
                                         msg=f"Content mismatch in {expected_filename} at line {i}")
                print(f"Test Passed: {expected_filename} verified successfully (Extracted ID: {extracted_id})")
            else:
                print(f"Warning: Golden file for comparison is missing: {golden_picklist_fp}")

if __name__ == "__main__":
    unittest.main()