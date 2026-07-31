#!/usr/bin/env node
/**
 * Pretty-print a JSON file in place with 2-space indentation.
 * Usage: node format_json.js <path-to-json-file>
 */
const fs = require("fs");

const path = process.argv[2];
if (!path) {
  console.error("Usage: node format_json.js <path-to-json-file>");
  process.exit(1);
}

const raw = fs.readFileSync(path, "utf8");

let data;
try {
  data = JSON.parse(raw);
} catch (e) {
  console.error(`Invalid JSON in ${path}: ${e.message}`);
  process.exit(1);
}

fs.writeFileSync(path, JSON.stringify(data, null, 2) + "\n");
console.log(`Formatted ${path}`);
