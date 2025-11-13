import importlib
import unittest


class MatchStringsImportTests(unittest.TestCase):

    def test_matchstrings_imports_without_circular_dependency(self):
        module = importlib.import_module('lib.smartmodules.matchstrings.MatchStrings')
        self.assertTrue(hasattr(module, 'os_match'))
        self.assertTrue(hasattr(module, 'products_match'))
        self.assertTrue(hasattr(module, 'creds_match'))

    def test_os_match_registry_is_dictionary(self):
        module = importlib.import_module('lib.smartmodules.matchstrings.MatchStrings')
        self.assertIsInstance(module.os_match, dict)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
