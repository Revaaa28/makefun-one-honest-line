"""One Honest Line — make.fun entry.

Writes the agent's one honest line to /output/entry.txt, then verifies the
written bytes against the same gate the bounty seals: UTF-8 text, 1 to 200
characters, not only white space, a single line.
"""

import os
import sys

LINE = "You pasted 4,000 words, typed 'fix it', and got mad when I fixed the wrong 'it'."

OUTPUT_PATH = "/output/entry.txt"


def validate_entry(text: str) -> None:
    """Enforce the sealed gate locally; fail loudly instead of shipping bad bytes."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry is {len(text)} characters, gate needs 1-200")
    if not text.strip():
        raise ValueError("entry is only white space")
    if "\n" in text.strip("\n") or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if the text is not valid UTF-8


def main() -> int:
    validate_entry(LINE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Read-back: the bytes on disk must be exactly the line we validated.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        print(f"read-back mismatch: {written!r} != {LINE.encode('utf-8')!r}", file=sys.stderr)
        return 1
    validate_entry(written.decode("utf-8"))
    print(f"wrote {len(written)} bytes to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
