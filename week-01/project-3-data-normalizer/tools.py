import csv
import json
import os
import re
from datetime import datetime

from rules import (
    COLUMN_ALIASES,
    VALUE_MAPPINGS,
    FORMAT_RULES,
    NULL_INDICATORS,
    DUPLICATE_KEYS,
)

# Shared dataset state for the agent tools
DATAFRAME = []
HEADERS = []
AUDIT_LOG = []

# ─────────────────────────────────────────────
# TOOL SCHEMAS
# ─────────────────────────────────────────────
TOOL_SCHEMAS = [
    {
        "name": "profile_data",
        "description": (
            "Analyze the loaded dataset and report column naming issues, inconsistent values, bad formats, null markers, duplicates, and any other data quality problems."
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "normalize_columns",
        "description": (
            "Normalize column names using predefined aliases and standard snake_case naming."
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "normalize_values",
        "description": (
            "Normalize values in the dataset according to column-specific value mappings."
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "fix_formats",
        "description": (
            "Fix common formats such as dates, phone numbers, and text casing in the loaded dataset."
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "flag_nulls",
        "description": (
            "Replace null-like values with proper null entries and report which columns were normalized."
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "detect_duplicates",
        "description": (
            "Detect duplicate rows based on the configured duplicate key columns and mark them in the dataset."
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "export_clean_csv",
        "description": ("Export the cleaned dataset to a CSV file."),
        "input_schema": {
            "type": "object",
            "properties": {
                "output_path": {
                    "type": "string",
                    "description": "Optional path for the cleaned CSV output.",
                }
            },
            "required": [],
        },
    },
    {
        "name": "export_audit_report",
        "description": (
            "Export a JSON audit report describing every change made during normalization."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "output_path": {
                    "type": "string",
                    "description": "Optional path for the audit report output.",
                }
            },
            "required": [],
        },
    },
]


def snake_case(value: str) -> str:
    value = value.strip()
    value = re.sub(r"[^0-9a-zA-Z]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_").lower()


def normalize_null_marker(value: str):
    if value is None:
        return None
    normalized = str(value).strip()
    if normalized == "":
        return None
    if normalized.lower() in {item.lower() for item in NULL_INDICATORS}:
        return None
    return value


def normalize_value(column: str, value: str):
    if value is None:
        return None

    text = str(value).strip()
    if text == "":
        return None

    lower = text.lower()
    if column in VALUE_MAPPINGS:
        for key, mapped in VALUE_MAPPINGS[column].items():
            if lower == key.lower():
                return mapped

    if column in FORMAT_RULES.get("text_columns", []):
        return text.title()

    return text


def normalize_phone(value: str):
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None

    if text.lower() in {item.lower() for item in NULL_INDICATORS}:
        return None

    digits = re.sub(r"\D+", "", text)
    if digits.startswith("001"):
        digits = digits[3:]
    if digits.startswith("1") and len(digits) == 11:
        digits = digits[1:]
    if len(digits) == 10:
        return "+1" + digits
    if len(digits) >= 11 and digits.startswith("+"):
        return "+" + digits
    if len(digits) >= 11:
        return "+" + digits
    return text


def normalize_date(value: str):
    if value is None:
        return None

    text = str(value).strip()
    if text == "":
        return None

    if text.lower() in {item.lower() for item in NULL_INDICATORS}:
        return None

    date_formats = [
        "%Y-%m-%d",
        "%m/%d/%y",
        "%m/%d/%Y",
        "%Y.%m.%d",
        "%B %d %Y",
        "%b %d %Y",
        "%d-%b-%Y",
        "%m-%d-%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
    ]

    normalized = text.replace(".", "-").replace("/", "-")
    normalized = re.sub(r"\s+", " ", normalized)
    for fmt in date_formats:
        try:
            parsed = datetime.strptime(text, fmt)
            return parsed.date().isoformat()
        except ValueError:
            pass
    try:
        parsed = datetime.fromisoformat(text)
        return parsed.date().isoformat()
    except ValueError:
        pass

    return text


def load_csv(input_path: str) -> str:
    global DATAFRAME, HEADERS, AUDIT_LOG

    with open(input_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        HEADERS = reader.fieldnames or []
        DATAFRAME = [row for row in reader]

    AUDIT_LOG = [
        {
            "step": "load_csv",
            "detail": f"Loaded {len(DATAFRAME)} rows from {input_path}",
            "headers": HEADERS,
        }
    ]
    return f"Loaded {len(DATAFRAME)} rows and {len(HEADERS)} columns."


def profile_data() -> str:
    problems = []
    seen_values = {}

    problems.append(f"Columns detected: {HEADERS}")

    for header in HEADERS:
        if header != snake_case(header):
            problems.append(
                f"Column naming issue: '{header}' should normalize to '{snake_case(header)}'"
            )

    for row_index, row in enumerate(DATAFRAME, start=1):
        for column, value in row.items():
            if value is None or str(value).strip().lower() in {
                item.lower() for item in NULL_INDICATORS
            }:
                problems.append(
                    f"Row {row_index} column '{column}' has null-like value '{value}'"
                )

            normalized_column = snake_case(column)
            if normalized_column in VALUE_MAPPINGS:
                lower = str(value).strip().lower()
                if (
                    lower
                    and lower
                    not in {k.lower() for k in VALUE_MAPPINGS[normalized_column].keys()}
                    and lower
                    not in {
                        v.lower() for v in VALUE_MAPPINGS[normalized_column].values()
                    }
                ):
                    problems.append(
                        f"Row {row_index} column '{column}' has inconsistent value '{value}'"
                    )

            if normalized_column in FORMAT_RULES.get("date_columns", []):
                if (
                    isinstance(value, str)
                    and value.strip()
                    and normalize_date(value) == value
                ):
                    problems.append(
                        f"Row {row_index} column '{column}' may have a bad date format: '{value}'"
                    )

    duplicate_counts = {}
    for row in DATAFRAME:
        key = tuple(row.get(col, "") for col in DUPLICATE_KEYS)
        duplicate_counts[key] = duplicate_counts.get(key, 0) + 1
    duplicates = sum(1 for count in duplicate_counts.values() if count > 1)
    if duplicates:
        problems.append(
            f"Detected {duplicates} duplicate row sets using keys {DUPLICATE_KEYS}"
        )

    if not problems:
        problems.append("No obvious profiling issues detected.")

    return "\n".join(problems)


def normalize_columns() -> str:
    global DATAFRAME, HEADERS, AUDIT_LOG
    rename_map = {}
    for header in HEADERS:
        normalized = COLUMN_ALIASES.get(header, snake_case(header))
        if normalized != header:
            rename_map[header] = normalized

    if not rename_map:
        return "No column names required normalization."

    for row in DATAFRAME:
        for old_name, new_name in rename_map.items():
            row[new_name] = row.pop(old_name)

    HEADERS = [rename_map.get(header, header) for header in HEADERS]
    AUDIT_LOG.append(
        {"step": "normalize_columns", "detail": f"Renamed columns: {rename_map}"}
    )
    return f"Normalized columns: {rename_map}."


def normalize_values() -> str:
    global DATAFRAME, AUDIT_LOG
    changes = []
    for row_index, row in enumerate(DATAFRAME, start=1):
        for column, value in list(row.items()):
            normalized_column = snake_case(column)
            if (
                normalized_column in VALUE_MAPPINGS
                or normalized_column in FORMAT_RULES.get("text_columns", [])
            ):
                new_value = normalize_value(
                    normalized_column, normalize_null_marker(value)
                )
                if new_value != value:
                    changes.append(
                        {
                            "row": row_index,
                            "column": column,
                            "from": value,
                            "to": new_value,
                        }
                    )
                    row[column] = new_value
    AUDIT_LOG.append(
        {
            "step": "normalize_values",
            "detail": f"Applied {len(changes)} value normalizations.",
            "changes": changes,
        }
    )
    return f"Applied value normalizations to {len(changes)} cells."


def fix_formats() -> str:
    global DATAFRAME, AUDIT_LOG
    changes = []
    for row_index, row in enumerate(DATAFRAME, start=1):
        for column, value in list(row.items()):
            normalized_column = snake_case(column)
            if normalized_column in FORMAT_RULES.get("date_columns", []):
                cleaned = normalize_date(value)
            elif normalized_column in FORMAT_RULES.get("phone_columns", []):
                cleaned = normalize_phone(value)
            elif normalized_column in FORMAT_RULES.get("text_columns", []):
                cleaned = normalize_value(
                    normalized_column, normalize_null_marker(value)
                )
            else:
                continue

            if cleaned != value:
                changes.append(
                    {"row": row_index, "column": column, "from": value, "to": cleaned}
                )
                row[column] = cleaned

    AUDIT_LOG.append(
        {
            "step": "fix_formats",
            "detail": f"Applied {len(changes)} format fixes.",
            "changes": changes,
        }
    )
    return f"Applied format fixes to {len(changes)} cells."


def flag_nulls() -> str:
    global DATAFRAME, AUDIT_LOG
    changes = []
    for row_index, row in enumerate(DATAFRAME, start=1):
        for column, value in list(row.items()):
            normalized = normalize_null_marker(value)
            if normalized is None and value not in (None, ""):
                changes.append(
                    {"row": row_index, "column": column, "from": value, "to": None}
                )
                row[column] = None
    AUDIT_LOG.append(
        {
            "step": "flag_nulls",
            "detail": f"Marked {len(changes)} null values.",
            "changes": changes,
        }
    )
    return f"Replaced {len(changes)} null-like values with proper nulls."


def detect_duplicates() -> str:
    global DATAFRAME, AUDIT_LOG
    seen = {}
    duplicate_rows = 0
    for row_index, row in enumerate(DATAFRAME, start=1):
        key = tuple((row.get(col) or "").strip().lower() for col in DUPLICATE_KEYS)
        if key in seen:
            row["duplicate_flag"] = "duplicate"
            duplicate_rows += 1
        else:
            row["duplicate_flag"] = "unique"
            seen[key] = row

    if "duplicate_flag" not in HEADERS:
        HEADERS.append("duplicate_flag")
    AUDIT_LOG.append(
        {
            "step": "detect_duplicates",
            "detail": f"Marked {duplicate_rows} duplicate rows using keys {DUPLICATE_KEYS}.",
        }
    )
    return f"Marked {duplicate_rows} duplicate rows."


def export_clean_csv(output_path: str = None) -> str:
    global DATAFRAME, HEADERS, AUDIT_LOG
    if output_path is None:
        output_path = "cleaned_sample.csv"

    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
        writer.writeheader()
        for row in DATAFRAME:
            writer.writerow(
                {key: ("" if value is None else value) for key, value in row.items()}
            )

    AUDIT_LOG.append(
        {"step": "export_clean_csv", "detail": f"Wrote cleaned CSV to {output_path}"}
    )
    return f"Cleaned CSV exported to {output_path}."


def export_audit_report(output_path: str = None) -> str:
    global AUDIT_LOG
    if output_path is None:
        output_path = "audit_sample.json"

    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(AUDIT_LOG, outfile, indent=2)

    AUDIT_LOG.append(
        {
            "step": "export_audit_report",
            "detail": f"Wrote audit report to {output_path}",
        }
    )
    return f"Audit report exported to {output_path}."


def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "profile_data":
        return profile_data()
    if tool_name == "normalize_columns":
        return normalize_columns()
    if tool_name == "normalize_values":
        return normalize_values()
    if tool_name == "fix_formats":
        return fix_formats()
    if tool_name == "flag_nulls":
        return flag_nulls()
    if tool_name == "detect_duplicates":
        return detect_duplicates()
    if tool_name == "export_clean_csv":
        return export_clean_csv(tool_input.get("output_path"))
    if tool_name == "export_audit_report":
        return export_audit_report(tool_input.get("output_path"))
    return f"Unknown tool: {tool_name}"
