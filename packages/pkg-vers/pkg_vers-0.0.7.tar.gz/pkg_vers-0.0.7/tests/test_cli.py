import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

# Ensure the package directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pkg_vers')))

# Import the __main__ module from pkg_vers
import pkg_vers.__main__ as main_module

class TestMain(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['__main__.py', 'get_versions', 'test_path1', 'test_path2'])
    @patch('pkg_vers.__main__.get_pkg_vers')
    def test_get_versions(self, mock_get_pkg_vers, mock_stdout):
        # Set up the mock return value
        mock_get_pkg_vers.return_value = {
            'package1': '1.0.0',
            'package2': '2.3.4'
        }

        # Call the main function to trigger the CLI
        main_module.main()

        # Define expected output
        expected_output = "package1: 1.0.0\npackage2: 2.3.4\n"

        # Get the actual output and strip any extra whitespace
        actual_output = mock_stdout.getvalue().strip()

        print(mock_stdout.getvalue())
        print(expected_output)
        # Check the actual output
        self.assertEqual(actual_output, expected_output.strip())

if __name__ == '__main__':
    unittest.main()
