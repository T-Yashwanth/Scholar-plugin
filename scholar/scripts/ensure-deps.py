#!/usr/bin/env python
"""Ensure python-docx is available to THIS interpreter.

Run from the SessionStart hook in exec form, so no shell is involved and
the same command works on Windows, macOS, and Linux.

The install targets sys.executable deliberately. A machine can easily have
several Pythons on PATH (for example `python` at 3.11 and `py` at 3.14), and
installing into the wrong one leaves generate-docx.py unable to import docx
even though pip reported success.
"""

import subprocess
import sys


def main() -> int:
    try:
        import docx  # noqa: F401
    except ImportError:
        pass
    else:
        print("scholar: python-docx ready")
        return 0

    print("scholar: installing python-docx...")
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pip", "install", "python-docx", "--quiet"],
            capture_output=True,
            text=True,
            timeout=100,
        )
    except subprocess.TimeoutExpired:
        print("scholar: python-docx install timed out. "
              "Run: python -m pip install python-docx")
        return 0
    except Exception as exc:  # pragma: no cover - defensive
        print("scholar: could not run pip (%s). "
              "Run: python -m pip install python-docx" % exc)
        return 0

    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip().splitlines()
        print("scholar: python-docx install failed. "
              "Run: python -m pip install python-docx")
        if detail:
            print("scholar: pip said: %s" % detail[-1][:200])
        return 0

    print("scholar: python-docx installed")
    return 0


if __name__ == "__main__":
    # Always exit 0. A dependency problem must not block the session; the
    # drafting skill degrades to markdown and reports the install command.
    sys.exit(main())
