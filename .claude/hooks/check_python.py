"""PostToolUse hook: after Claude edits a .py file, make sure it still compiles.

Exit code 2 sends the error back to Claude so it fixes the file right away.
Needs no database, so it's fast and safe to run on every edit.
"""
import json
import py_compile
import sys

payload = json.load(sys.stdin)
path = payload.get("tool_input", {}).get("file_path", "")

if not path.endswith(".py"):
    sys.exit(0)

try:
    py_compile.compile(path, doraise=True)
except py_compile.PyCompileError as err:
    print(f"Syntax error after edit in {path}:\n{err.msg}", file=sys.stderr)
    sys.exit(2)
