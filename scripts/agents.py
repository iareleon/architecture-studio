#!/usr/bin/env python3
"""agents.py — DEPRECATED wrapper for skillmanager

This command has been renamed to 'skillmanager'.
This wrapper will be removed in a future version.

Update any scripts or aliases that call 'agents' to use 'skillmanager' instead.
"""

import os
import sys
from pathlib import Path

print("[DEPRECATED] The 'agents' command has been renamed to 'skillmanager'.", file=sys.stderr)
print("             Update your scripts and aliases. This wrapper will be removed in a future version.\n", file=sys.stderr)

script_dir = Path(__file__).resolve().parent
skillmanager = script_dir / "skillmanager.py"

os.execv(sys.executable, [sys.executable, str(skillmanager)] + sys.argv[1:])
