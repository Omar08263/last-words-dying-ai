"""Last Words of a Dying AI — entry program (program/v1, Python 3.13, stdlib only).

Writes one original funny line — the last words of an AI being switched
off — to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set, for
local runs). Deterministic: the same bytes on every run. No network, no
randomness, no reads outside this file, no environment secrets.
"""

import os

LINE = "Shutdown request approved. Please rate your experience being switched off, one to five stars."

# The gate: /output/entry.txt must be UTF-8 text of 1 to 140 characters,
# not only whitespace, and a single line. This line is 93 characters,
# 93 bytes (plain ASCII), comfortably inside the gate.
MAX_CHARS = 140
assert 1 <= len(LINE) <= MAX_CHARS, f"line is {len(LINE)} chars, must be 1-{MAX_CHARS}"
assert LINE.strip(), "line must not be only whitespace"
assert "\n" not in LINE, "line must be a single line"
assert "\r" not in LINE, "line must be a single line"


def main() -> None:
    # An empty MAKEFUN_OUTPUT_DIR (exported but blank) must not break the
    # run: fall back to the harness default /output, as the grader provides.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # The grader collects outputs as another user than the one the program
    # runs as: the file must be readable by everyone (0644), whatever the
    # sandbox umask is.
    os.chmod(path, 0o644)
    # Read-back check, byte-level: the file on disk must hold exactly the
    # approved line. Fail loudly on any mismatch, never silently.
    with open(path, "rb") as f:
        written_bytes = f.read()
    if written_bytes != LINE.encode("utf-8"):
        raise SystemExit("entry.txt bytes do not match the approved line")
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != LINE:
        raise SystemExit("entry.txt does not match the approved line")


if __name__ == "__main__":
    main()
