import os
import tempfile
import unittest
import nbformat
from nbformat.v4 import new_notebook, new_code_cell
from pkg_vers.package_manager import _get_imported_top_level_packages_from_ipynb

class TestGetImportedPackages(unittest.TestCase):
    def create_notebook(self, cells):
        notebook = new_notebook()
        notebook.cells.extend(cells)
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ipynb') as temp_file:
            nbformat.write(notebook, temp_file)
            temp_file_path = temp_file.name
        return temp_file_path

    def test_get_imported_packages_from_ipynb(self):
        cells = [
            new_code_cell(source='import numpy as np\nimport pandas as pd'),
            new_code_cell(source='from sklearn.model_selection import train_test_split'),
            new_code_cell(source='import matplotlib.pyplot as plt')
        ]
        temp_file_path = self.create_notebook(cells)
        imported_packages = _get_imported_top_level_packages_from_ipynb(temp_file_path)
        expected_packages = {'numpy', 'pandas', 'sklearn', 'matplotlib'}
        self.assertEqual(imported_packages, expected_packages)
        os.unlink(temp_file_path)
    
    def test_relative_imports(self):
        cells = [
            new_code_cell(source='from . import mymodule\nimport numpy as np\nfrom sklearn import datasets')
        ]
        temp_file_path = self.create_notebook(cells)
        imported_packages = _get_imported_top_level_packages_from_ipynb(temp_file_path)
        print(f"imported_packages: {imported_packages}")
        expected_packages = {'numpy', 'sklearn'}
        self.assertEqual(imported_packages, expected_packages)
        os.unlink(temp_file_path)


if __name__ == '__main__':
    unittest.main()
