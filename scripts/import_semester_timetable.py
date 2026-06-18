#!/usr/bin/env python3
"""
Convert the semester overview Excel file into chatbot knowledge Markdown.

The Excel file is a visual weekly timetable. This script extracts the non-empty
entries into a searchable list that the chatbot can use for enrolled students.
"""

from __future__ import annotations

import argparse
import re
import zipfile
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "knowledge_docs/Semesteruebersicht_SS26.md"
NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import an SS26 Excel timetable into knowledge_docs.")
    parser.add_argument("xlsx", help="Path to the semester overview .xlsx file.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Markdown output path.")
    return parser.parse_args()


def column_number(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref)
    if not match:
        return 1
    number = 0
    for char in match.group(1):
        number = number * 26 + ord(char) - 64
    return number


def excel_date(value: str) -> str:
    try:
        serial = int(float(value))
    except ValueError:
        return value
    date = datetime(1899, 12, 30) + timedelta(days=serial)
    return date.strftime("%Y-%m-%d")


def clean_cell(value: str) -> str:
    value = value.replace("\r", "\n")
    value = re.sub(r"\n+", " / ", value)
    return re.sub(r"\s+", " ", value).strip()


def read_sheet(path: Path) -> dict[int, dict[int, str]]:
    with zipfile.ZipFile(path) as workbook:
        shared_strings = []
        if "xl/sharedStrings.xml" in workbook.namelist():
            root = ElementTree.fromstring(workbook.read("xl/sharedStrings.xml"))
            for item in root.findall("a:si", NS):
                shared_strings.append("".join(text.text or "" for text in item.findall(".//a:t", NS)))

        sheet = ElementTree.fromstring(workbook.read("xl/worksheets/sheet1.xml"))
        rows: dict[int, dict[int, str]] = {}
        for row in sheet.findall(".//a:sheetData/a:row", NS):
            row_index = int(row.attrib["r"])
            row_values: dict[int, str] = {}
            for cell in row.findall("a:c", NS):
                ref = cell.attrib.get("r", "A1")
                col_index = column_number(ref)
                value_node = cell.find("a:v", NS)
                if value_node is None or value_node.text is None:
                    continue
                value = value_node.text
                if cell.attrib.get("t") == "s":
                    value = shared_strings[int(value)]
                row_values[col_index] = clean_cell(value)
            rows[row_index] = row_values
        return rows


def parse_block(value: str) -> tuple[str, str]:
    match = re.match(r"(\d+)\s*/?\s*\(([^)]+)\)", value)
    if not match:
        return value, ""
    return match.group(1), match.group(2)


def timetable_events(rows: dict[int, dict[int, str]]) -> list[dict[str, str]]:
    day_row = rows.get(2, {})
    header_row = rows.get(3, {})
    day_starts = sorted(col for col, value in day_row.items() if value)
    day_starts.append(10_000)

    events = []
    current_dates: dict[int, str] = {}
    for row_index in sorted(row for row in rows if row >= 4):
        row = rows[row_index]
        for position, start_col in enumerate(day_starts[:-1]):
            end_col = day_starts[position + 1]
            day_name = day_row.get(start_col, "")
            date_value = row.get(start_col)
            if date_value:
                current_dates[start_col] = excel_date(date_value)
            date = current_dates.get(start_col)
            block_text = row.get(start_col + 1, "")
            if not date or not block_text:
                continue
            block, time_range = parse_block(block_text)

            for col_index in range(start_col + 2, end_col):
                audience = header_row.get(col_index, "")
                entry = row.get(col_index, "")
                if not audience or not entry:
                    continue
                if audience.lower() in {"datum", "block"}:
                    continue
                events.append(
                    {
                        "date": date,
                        "day": day_name,
                        "block": block,
                        "time": time_range,
                        "audience": audience,
                        "entry": entry,
                    }
                )
    return events


def write_markdown(events: list[dict[str, str]], output: Path, source_name: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Semester Timetable SS26",
        "",
        f"Source file: {source_name}",
        "",
        "This timetable is for enrolled MEM and MIM students. It includes MEM / 1, MEM / 2, MIM / 1, MIM / 2, and MIM E-Track entries.",
        "",
        "Use it to answer questions about class dates, events, time blocks, course sessions, holidays, and timetable entries.",
        "",
        "| Date | Day | Block | Time | Audience | Event / class |",
        "|---|---|---:|---|---|---|",
    ]
    for event in events:
        lines.append(
            "| {date} | {day} | {block} | {time} | {audience} | {entry} |".format(
                **{key: value.replace("|", "/") for key, value in event.items()}
            )
        )

    lines.extend(
        [
            "",
            "## Timetable Notes",
            "",
            "- `MIM E-Track` means the MIM English-taught track.",
            "- `MEM / 1` and `MIM / 1` refer to first-semester groups.",
            "- `MEM / 2` and `MIM / 2` refer to second-semester groups.",
            "- Students should still check official announcements and email updates for last-minute changes.",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    source = Path(args.xlsx)
    if not source.exists():
        raise SystemExit(f"Excel file not found: {source}")

    rows = read_sheet(source)
    events = timetable_events(rows)
    output = Path(args.output)
    write_markdown(events, output, source.name)
    print(f"Imported {len(events)} timetable entries into {output}")


if __name__ == "__main__":
    main()
