---
name: format-json
description: Formats an unformatted/minified JSON file into readable, indented JSON. Use when the user asks to format, pretty-print, beautify, or indent a JSON file, or mentions a JSON file that is "unformatted", "minified", "all on one line", or "hard to read".
---

# Format JSON

Reformat a JSON file into readable, consistently indented JSON, in place (or to a new file if the user asks for one).

## Steps

1. Identify the target JSON file. If the user didn't name one, look for `.json` files in the current project and ask which one if there's more than one candidate.
2. Read the file and validate it is parseable JSON. If it fails to parse, report the exact parse error (message + position) instead of guessing at a fix.
3. Pretty-print it with 2-space indentation and a trailing newline, preserving key order (do not sort keys unless asked).
4. Write the formatted result back to the same file path (unless the user asked for a different output path).
5. Show the user a short diff-style summary (e.g. before/after line count) rather than dumping the whole file back at them.

## Implementation

Run whichever script matches a runtime already available in the project — do not add a new dependency just to pretty-print JSON:

- Python: `python scripts/format_json.py <path-to-json-file>`
- Node: `node scripts/format_json.js <path-to-json-file>`

Both scripts validate the JSON, report a parse error and exit non-zero if it's invalid, otherwise rewrite the file in place with 2-space indentation and a trailing newline.

## Notes

- Never silently "fix" invalid JSON (e.g. trailing commas, comments) by deleting content — flag it to the user and ask before making structural changes beyond whitespace/formatting.
- Keep number/string formatting as-is; this skill only changes whitespace/indentation, not values.
