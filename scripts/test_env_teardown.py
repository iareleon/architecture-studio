#!/usr/bin/env python3
"""test_env_teardown.py — remove the Skill Forge test environment

Removes:
  .tmp-skillmanager/               temporary install directory
  LLM symlinks listed in .test-manifest (test-created links ONLY)

Production skill dirs and symlinks are never touched.
Only symlinks recorded in .test-manifest are removed.

Usage:
  python3 scripts/test_env_teardown.py
"""

import os
import sys
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

def _supports_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("TERM", "") != "dumb"

if _supports_color():
    BOLD   = "\033[1m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    CYAN   = "\033[36m"
    RESET  = "\033[0m"
else:
    BOLD = GREEN = YELLOW = CYAN = RESET = ""


def info(msg: str) -> None:
    print(f"{CYAN}[INFO]{RESET}  {msg}")

def ok(msg: str) -> None:
    print(f"{GREEN}[OK]{RESET}    {msg}")

def warn(msg: str) -> None:
    print(f"{YELLOW}[WARN]{RESET}  {msg}", file=sys.stderr)

def header(msg: str) -> None:
    print(f"\n{BOLD}{msg}{RESET}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent

    tmp_skillmanager_dir = repo_root / ".tmp-skillmanager"
    test_manifest = tmp_skillmanager_dir / ".test-manifest"

    header("Test Environment Teardown")
    print(f"\nTMP_SKILLMANAGER_DIR = {tmp_skillmanager_dir}\n")

    # -----------------------------------------------------------------------
    # Step 1 — Remove test symlinks recorded in .test-manifest
    # -----------------------------------------------------------------------
    header("Removing test symlinks (manifest-tracked only)")

    if test_manifest.exists():
        for link_str in test_manifest.read_text(encoding="utf-8").splitlines():
            link_str = link_str.strip()
            if not link_str:
                continue
            link = Path(link_str)
            if link.is_symlink():
                link.unlink()
                ok(f"Removed: {link}")
            else:
                info(f"Not a symlink (already removed?): {link}")
        ok(f"Manifest processed: {test_manifest}")
    else:
        info("No manifest found — no test symlinks to remove.")

    # -----------------------------------------------------------------------
    # Step 2 — Remove the tmp install directory
    # -----------------------------------------------------------------------
    header("Removing test install directory")

    if tmp_skillmanager_dir.is_dir():
        shutil.rmtree(tmp_skillmanager_dir, ignore_errors=True)
        ok(f"Removed: {tmp_skillmanager_dir}")
    else:
        info(f"Not found (already clean): {tmp_skillmanager_dir}")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    header("Teardown Complete")
    print()
    print("Production skills and symlinks were not modified.")
    print("If TMP_SKILLMANAGER_DIR is exported in your shell, unset it with:")
    if sys.platform == "win32":
        print("\n  set TMP_SKILLMANAGER_DIR=\n")
    else:
        print("\n  unset TMP_SKILLMANAGER_DIR\n")


if __name__ == "__main__":
    main()
