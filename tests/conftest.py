"""Test configuration helpers."""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

# Ensure repository root is importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message=r"invalid escape sequence",
)
