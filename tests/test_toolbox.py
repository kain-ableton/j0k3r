import unittest

from lib.core.Exceptions import SettingsException
from lib.core.Tool import Tool
from lib.core.Toolbox import Toolbox


class ToolboxIndexTests(unittest.TestCase):

    def setUp(self):
        self.toolbox = Toolbox(settings=None, services=['multi', 'http'])

    def _make_tool(self, name, service='multi'):
        return Tool(
            name=name,
            description='desc',
            target_service=service,
            installed=False,
        )

    def test_get_tool_returns_cached_instance(self):
        tool = self._make_tool('ExampleTool')
        self.toolbox.add_tool(tool)

        retrieved = self.toolbox.get_tool('exampletool')
        self.assertIs(retrieved, tool)

    def test_duplicate_tool_name_raises(self):
        self.toolbox.add_tool(self._make_tool('ExampleTool'))

        with self.assertRaises(SettingsException):
            self.toolbox.add_tool(self._make_tool('ExampleTool', service='http'))

    def test_unknown_service_raises(self):
        with self.assertRaises(SettingsException):
            self.toolbox.add_tool(self._make_tool('WrongService', service='smtp'))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
