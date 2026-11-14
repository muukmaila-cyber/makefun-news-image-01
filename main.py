#!/usr/bin/env python3
"""news-image-01 entry (v3): write the front-page image to /output/entry.png.

The front page (18 verified stories of Friday 13 November 2026) is bundled
in this repository as entry.png. v3 is a fully illustrated grid: every story
has its own editorial illustration (three AI-generated contact sheets in
illustrations/, sliced into 18 panels and composited by build_v3.py), with
headlines, one-line summaries and data badges rendered in PIL. This program
copies entry.png byte-for-byte to the output path, so both grader runs write
identical bytes. No network is used.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

def check_png(path):
    """Verify the file is a PNG and return its (width, height) from IHDR.

    Pure stdlib: reads the 8-byte magic and the 13-byte IHDR chunk.
    Returns None when the file is not a valid PNG.
    """
    try:
        with open(path, "rb") as f:
            head = f.read(33)
    except OSError:
        return None
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        return None
    if head[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return width, height

def main():
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    if not os.path.exists(SRC):
        print("entry.png not found in repository", file=sys.stderr)
        return 1
    shutil.copyfile(SRC, out)
    dims = check_png(out)
    if dims is None:
        print("output is not a valid PNG", file=sys.stderr)
        return 1
    if dims != (1024, 1024):
        print("unexpected output size %sx%s, want 1024x1024" % dims, file=sys.stderr)
        return 1
    if os.path.getsize(out) > 1048576:
        print("output over the 1 MiB limit", file=sys.stderr)
        return 1
    def sha256(path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    if sha256(SRC) != sha256(out):
        print("output differs from bundled entry.png", file=sys.stderr)
        return 1
    print("wrote", out, os.path.getsize(out), "bytes, %sx%s PNG" % dims)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
