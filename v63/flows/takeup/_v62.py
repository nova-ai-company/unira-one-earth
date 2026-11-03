"""Import the V6.2 fetch/jsonstat helpers without copying them (read-only reuse)."""
import sys
from pathlib import Path

V62_SRC = Path(__file__).resolve().parents[3] / "v62" / "src"
if str(V62_SRC) not in sys.path:
    sys.path.insert(0, str(V62_SRC))

from unira_v62 import fetch, jsonstat  # noqa: E402,F401
