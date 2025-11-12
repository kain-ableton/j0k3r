import io
import sys
import unittest
from contextlib import redirect_stdout

from lib.core.ProcessLauncher import ProcessLauncher


class ProcessLauncherTests(unittest.TestCase):

    def test_sequence_command_streams_output(self):
        launcher = ProcessLauncher([sys.executable, '-c', 'print("hello")'], shell=False)
        with redirect_stdout(io.StringIO()) as buffer:
            code, output = launcher.start()

        self.assertEqual(code, 0)
        self.assertEqual(buffer.getvalue(), 'hello\n')
        self.assertIn('hello', output)

    def test_environment_overrides(self):
        launcher = ProcessLauncher(
            [sys.executable, '-c', 'import os; print(os.environ.get("FOO"))'],
            env={'FOO': 'BAR'},
            shell=False,
        )
        with redirect_stdout(io.StringIO()) as buffer:
            code, output = launcher.start()

        self.assertEqual(code, 0)
        self.assertIn('BAR', output)
        self.assertEqual(buffer.getvalue().strip(), 'BAR')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
