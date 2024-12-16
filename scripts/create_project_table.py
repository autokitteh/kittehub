"""Extract metadata from project README files to update table in repo's README file."""

import os
from pathlib import Path
import re
import yaml

ROOT_PATH = Path(__file__).parent.parent
README_PATH = ROOT_PATH / "README.md"


def extract_metadata(readme_file: Path) -> dict:
    """Extract metadata from a README file."""
    metadata = {}
    lines = readme_file.read_text(encoding="utf-8").splitlines()

    # Check for metadata block at the top of the README
    if lines[0].strip() == "---":
        metadata_lines = []
        for line in lines[1:]:
            if line.strip() == "---":
                break
            metadata_lines.append(line)

        metadata = yaml.safe_load("\n".join(metadata_lines))

    return metadata


def to_table_row(readme_file: Path, metadata: dict) -> str:
    """Convert metadata into a markdown table row."""
    title = metadata.get("title", "")
    if not title:
        return ""

    description = metadata.get("description", "")
    integrations = ", ".join(metadata.get("integrations", [])) or "None"
    relative_path = os.path.relpath(os.path.dirname(readme_file), ROOT_PATH)
    link = f"./{relative_path}/"

    return f"| [{title}]({link}) | {description} | {integrations} |\n"


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
    headers = "-->\n| Name | Description | Integration |\n| :--- | :---------- | :---------- |\n<!--"
    md = re.sub("-->.+<!--", headers, md, flags=re.DOTALL)

    lines = readme_file.read_text(encoding="utf-8").splitlines(keepends=True)

    start_marker_index = next(
        i for i, line in enumerate(lines) if line.strip() == "<!-- START-TABLE -->"
    )
    end_marker_index = next(
        i for i, line in enumerate(lines) if line.strip() == "<!-- END-TABLE -->"
    )

    # Replace content between the markers
    updated_lines = (
        lines[: start_marker_index + 3]
        + [line if line.endswith("\n") else f"{line}\n" for line in new_rows]
        + lines[end_marker_index:]
    )
    readme_file.write_text("".join(updated_lines), encoding="utf-8")


if __name__ == "__main__":
    new_rows = generate_readme_table(ROOT_PATH)
    insert_rows_to_table(README_PATH, new_rows)
