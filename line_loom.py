#!/usr/bin/env python3
"""Inspect and normalize line endings in UTF-8 text files."""
import argparse
from pathlib import Path


def inspect(data):
    crlf = data.count(b"\r\n")
    return {"CRLF": crlf, "LF": data.count(b"\n") - crlf, "CR": data.count(b"\r") - crlf}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--to", choices=("lf", "crlf"))
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    if bool(args.to) != bool(args.output):
        parser.error("--to and --output must be used together")
    try:
        data = args.file.read_bytes()
        data.decode("utf-8-sig")
        if b"\0" in data:
            raise ValueError("file contains NUL bytes")
        if args.output:
            normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            if args.to == "crlf":
                normalized = normalized.replace(b"\n", b"\r\n")
            with args.output.open("xb") as output:
                output.write(normalized)
        else:
            for style, count in inspect(data).items():
                print(f"{style:<4} {count}")
            final_ending = data.endswith((b'\r', b'\n'))
            print(f"Final line ending: {'yes' if final_ending else 'no'}")
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
