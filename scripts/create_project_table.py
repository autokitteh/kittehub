"""Extract metadata from project README files to update table in repo's README file."""

import os
from pathlib import Path
import re

ROOT_PATH = Path(__file__).parent.parent
README_PATH = ROOT_PATH / "README.md"


def extract_metadata(readme_file: Path) -> dict:
    """Extract metadata from a project's README file."""
    field_pattern = r"^([a-z]+):\s+(.+)$"
    elements_pattern = r'"(.+?)"'
    f = readme_file.read_text(encoding="utf-8")
    metadata = {}

    for k, v in re.findall(field_pattern, f, re.MULTILINE):
        if k == "integrations":
            metadata[k] = re.findall(elements_pattern, v)
        else:
            metadata[k] = v

    return metadata


def to_table_row(readme_file: Path, metadata: dict) -> str:
    """Convert metadata into a markdown table row."""
    title = metadata.get("title", "")
    if not title:
        return ""

    description = metadata.get("description", "")
    integrations = ", ".join(metadata.get("integrations", []))
    path = os.path.relpath(os.path.dirname(readme_file), ROOT_PATH)

    return f"| [{title}](./{path}/) | {description} | {integrations} |\n"


def generate_readme_table(folder_path: Path) -> list[str]:
    """Generate a list of table rows from README metadata."""
    rows = []
    for readme_file in folder_path.rglob("README.md"):
        metadata = extract_metadata(readme_file)
        row = to_table_row(readme_file, metadata)
        if row:
            rows.append(row)
    return rows


def insert_rows_to_table(readme_file: Path, new_rows: list[str]) -> None:
    """Insert rows into the table section of the README file."""
    md = readme_file.read_text(encoding="utf-8")
    table = "-->\n| Name | Description | Integration |\n| :--- | :---------- | :---------- |\n"

    for row in new_rows:
        table += row

    md = re.sub("-->.+<!--", table + "<!--", md, flags=re.DOTALL)
    readme_file.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    new_rows = generate_readme_table(ROOT_PATH)
    insert_rows_to_table(README_PATH, new_rows)
