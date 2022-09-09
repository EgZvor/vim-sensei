#!/usr/bin/python

from contextlib import suppress
import argparse
import hashlib
import itertools
import json
import sys
from datetime import datetime
from pathlib import Path

GENERATED_NOTICE = "# Converted with ipynb-to-py.py on {}\n\n"
HASH_PATH = ".ipynb.hash.md5"


def updated_hash(new):
    old_hash = None
    with suppress(FileNotFoundError), open(HASH_PATH, "r", encoding="utf-8") as f:
        old_hash = f.read()

    new_hash = hashlib.md5(new.encode("utf-8")).hexdigest()

    if new_hash != old_hash:
        with open(HASH_PATH, "w", encoding="utf-8") as f:
            f.write(new_hash)
        return True

    return False


def main():
    prog = "python ipynb-to-py.py"
    description = "A command for converting Jupyter Notebook into one Python file."
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        "infile",
        type=argparse.FileType(encoding="utf-8"),
        help="Jupyter Notebook to dump the code from",
    )
    parser.add_argument(
        "outfile",
        type=Path,
        help="Python file to dump the code into",
    )

    options = parser.parse_args()

    with options.infile as infile:
        ipynb_content = infile.read()
        if not updated_hash(ipynb_content):
            print(
                "ipynb file did not change since last generation, ignoring...",
                file=sys.stderr,
            )
            return

        try:
            notebook = json.loads(ipynb_content)
        except ValueError as e:
            # pylint: disable=raise-missing-from
            raise SystemExit(e)

    source_lines = [
        GENERATED_NOTICE.format(datetime.today().strftime("%Y-%m-%d %H:%M")),
    ]
    source_lines.extend(
        itertools.chain.from_iterable(
            cell["source"] + ["\n\n"]
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )
    )

    with options.outfile.open("w", encoding="utf-8") as outfile:
        outfile.write("".join(source_lines).rstrip("\n"))
        outfile.write("\n")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError as exc:
        sys.exit(exc.errno)
