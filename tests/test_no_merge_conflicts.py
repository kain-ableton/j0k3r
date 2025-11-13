import unittest
from pathlib import Path


CONFLICT_PREFIXES = ("<<<<<<< ", ">>>>>>> ")
EXCLUDED_PATH_PREFIXES = (
    '.git',
    '__pycache__',
    'doc/_build',
    'docker',
    'pictures',
    'reports',
    'toolbox',
    'webshells',
)


def iter_repo_files(base_dir: Path):
    for path in base_dir.rglob('*'):
        if not path.is_file():
            continue
        relative_path = path.relative_to(base_dir).as_posix()
        if any(
            relative_path == prefix or relative_path.startswith(f"{prefix}/")
            for prefix in EXCLUDED_PATH_PREFIXES
        ):
            continue
        yield path


class MergeConflictMarkerTests(unittest.TestCase):

    def test_repository_has_no_conflict_markers(self):
        base_dir = Path(__file__).resolve().parents[1]
        offenders = {}

        for file_path in iter_repo_files(base_dir):
            try:
                contents = file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue

            offending_lines = []
            for idx, line in enumerate(contents.splitlines()):
                if any(line.startswith(prefix) for prefix in CONFLICT_PREFIXES):
                    offending_lines.append(idx + 1)

            if offending_lines:
                offenders[str(file_path.relative_to(base_dir))] = offending_lines

        self.assertFalse(
            offenders,
            msg=f"Merge conflict markers detected: {offenders}",
        )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
