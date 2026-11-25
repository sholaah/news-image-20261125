#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered entry.png into the output directory.

Stdlib only, no network, deterministic: the bytes copied are exactly the
bytes of entry.png shipped in this repository, so two runs are identical.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
