#!/usr/bin/env python3
"""Pretty-print a JSON file in place with 2-space indentation.

Usage: python format_json.py <path-to-json-file>
"""
import json
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python format_json.py <path-to-json-file>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in {path}: {e}", file=sys.stderr)
            sys.exit(1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2))
        f.write("\n")

    print(f"Formatted {path}")


if __name__ == "__main__":
    main()
