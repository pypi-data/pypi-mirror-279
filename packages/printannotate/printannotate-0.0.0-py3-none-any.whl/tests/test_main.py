import unittest
import sys
import os
from io import StringIO

from printannotate.traced_annotate import annotate

class TestPrintAnnotate(unittest.TestCase):

    def setUp(self):
        # Redirect stdout
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held

    def test_print_annotation(self):
        # Get the path to the test script
        file_dir = os.path.dirname(__file__)
        file_path = os.path.join(file_dir, 'test_scripts', 'fstrings.py')

        # Run the printannotate command on the test script
        output = annotate(file_path)

        # Check if the output contains the expected annotation
        annotated_file_path = file_path.replace('.py', '_annotated.py')

        with open(annotated_file_path) as file:
            annotated_script = file.read()

        # create one list from the output and the annotated script
        output_lines = output.splitlines()
        annotated_lines = annotated_script.splitlines()

        # Check if the output contains the expected annotation
        for output_line, annotated_line in zip(output_lines, annotated_lines):
            self.assertEqual(output_line, annotated_line)


if __name__ == "__main__":
    sys.stdout = sys.__stdout__
    unittest.main()
