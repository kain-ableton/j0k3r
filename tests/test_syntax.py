import py_compile
from pathlib import Path


def test_dbcontroller_has_valid_syntax(tmp_path):
    source = Path('lib/controller/DbController.py')
    compiled_path = tmp_path / 'DbController.pyc'
    py_compile.compile(str(source), cfile=str(compiled_path), doraise=True)
