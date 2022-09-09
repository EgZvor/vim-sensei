#!/usr/bin/python

import argparse
import itertools
import json
import sys
from datetime import datetime

GENERATED_NOTICE = "# Converted with ipynb-to-py.py on {}\n\n"


def main():
    prog = "python ipynb-to-py.py"
    description = "A command for converting Jupyter Notebook into one Python file."
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        "infile",
        nargs="?",
        type=argparse.FileType(encoding="utf-8"),
        help="Jupyter Notebook to dump the code from",
        default=sys.stdin,
    )

    options = parser.parse_args()

    with options.infile as infile:
        try:
            notebook = json.load(infile)
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

    print("".join(source_lines).rstrip("\n"))


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError as exc:
        sys.exit(exc.errno)
