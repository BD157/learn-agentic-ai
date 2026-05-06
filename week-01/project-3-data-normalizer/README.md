# Project 3 — Data Normalizer

This project is a data-driven agent that cleans messy CSV records and exports both a cleaned file and a JSON audit report.

The agent is designed to:
- Profile a CSV dataset for column issues, inconsistent values, bad formats, null markers, and duplicates
- Normalize column names to snake_case
- Normalize values by column (gender, country, status, etc.)
- Fix common formats like dates and phone numbers
- Replace bogus null markers with proper null values
- Detect duplicate rows and flag them
- Export a cleaned CSV plus a JSON audit report listing every change

---

## Run it

```bash
cd week-01/project-3-data-normalizer
python agent.py --input sample_data/sample.csv
```

The agent uses the same low-level ReAct style as Projects 1 and 2: raw Anthropic API, no LangChain or LangGraph.

---

## Files

```
project-3-data-normalizer/
├── README.md
├── agent.py
├── tools.py
├── rules.py
└── sample_data/
    └── sample.csv
```

---

## How it works

- `agent.py` loads the sample CSV and runs the ReAct loop against Claude.
- `tools.py` exposes data profiling, normalization, formatting, duplicate detection, and export tools.
- `rules.py` contains editable normalization rules for column aliases, value mappings, null indicators, formats, and duplicate keys.
- `sample_data/sample.csv` includes dirty input data with mixed casing, bad dates, inconsistent countries, phone variants, nulls, and a duplicate.

---

## Editing the rules

Open `rules.py` to customize:
- `COLUMN_ALIASES` for name normalization
- `VALUE_MAPPINGS` for value standardization
- `FORMAT_RULES` for date, phone, and text formatting
- `NULL_INDICATORS` for null-like values
- `DUPLICATE_KEYS` for duplicate detection

---

## Output files

When the agent runs, it writes:
- `cleaned_sample.csv` — the cleaned CSV output
- `audit_sample.json` — a JSON audit report with every change applied

If you want a different filename, call the export tools with `output_path` in the agent session.
