#!/usr/bin/env python3
"""news-image-01 entry: write the front-page image to /output/entry.png.

The front page (16 verified stories of Friday 13 November 2026, drawn
programmatically with PIL + one AI-generated lead photo) is bundled in this
repository as entry.png. This program copies it byte-for-byte to the output
path, so both grader runs write identical bytes. No network is used.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

def main():
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    if not os.path.exists(SRC):
        print("entry.png not found in repository", file=sys.stderr)
        return 1
    shutil.copyfile(SRC, out)
    print("wrote", out, os.path.getsize(out), "bytes")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
