#!/usr/bin/env python3
"""Wrapper — run 99_system/03_tools/sync_source_docs.py."""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parents[2] / "03_tools" / "sync_source_docs.py"))
