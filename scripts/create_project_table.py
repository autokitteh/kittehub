"""
Process README files to extract metadata, generate a table of content, 
and update a central README file with aggregated data.

- Extract metadata from the top section of the README file for each project (e.g., between "---" delimiters).
- Generate table rows summarizing the metadata
- Insert the generated rows into the project table in the main README file

Classes:
- ReadmeMetadataProcessor: Extracts and processes metadata from individual README files.
"""

import os
import yaml
from pathlib import Path
from typing import List

ROOT_PATH = Path(__file__).parent.parent
README_PATH = ROOT_PATH / "README.md"


class ReadmeMetadataProcessor:
    def __init__(self, readme_file: Path):
        self.readme_file = readme_file
        self.metadata = self.extract_metadata()

    def extract_metadata(self) -> dict:
        metadata = {}
        lines = self.readme_file.read_text(encoding="utf-8").splitlines()

        # Check for metadata block at the top of the README
        if lines[0].strip() == "---":
            metadata_lines = []
            for line in lines[1:]:
                if line.strip() == "---":
                    break
                metadata_lines.append(line)

            metadata = yaml.safe_load("\n".join(metadata_lines))

        return metadata

    def get_title(self) -> str:
        return self.metadata.get("title", None)

    def get_description(self) -> str:
        return self.metadata.get("description", "No description available.")

    def get_integrations(self) -> str:
        integrations = self.metadata.get("integrations", [])
        return ", ".join(integrations) if integrations else "None"

    def to_table_row(self) -> str:
        title = self.get_title()
        if not title:
            return ""

        description = self.get_description()
        integrations = self.get_integrations()
        relative_path = os.path.relpath(os.path.dirname(self.readme_file), ROOT_PATH)
        link = f"./{relative_path}/"

        return f"| [{title}]({link}) | {description} | {integrations} |\n"


def generate_readme_table(folder_path: Path) -> List[str]:
    """Generate a list of table rows from README metadata."""
    readme_files = folder_path.rglob("README.md")

    rows = []
    for readme_file in readme_files:
        processor = ReadmeMetadataProcessor(readme_file)
        row = processor.to_table_row()
        if row:
            rows.append(row)
    return rows


def insert_rows_to_table(readme_file: Path, new_rows: List[str]) -> None:
    """Insert rows into the table section of the README file."""
    lines = readme_file.read_text(encoding="utf-8").splitlines(keepends=True)

    start_marker_index = next(
        i for i, line in enumerate(lines) if line.strip() == "<!--start-table-->"
    )
    end_marker_index = next(
        i for i, line in enumerate(lines) if line.strip() == "<!--end-table-->"
    )

    # Replace content between the markers
    updated_lines = (
        lines[: start_marker_index + 3]
        + [line if line.endswith("\n") else f"{line}\n" for line in new_rows]
        + lines[end_marker_index:]
    )
    readme_file.write_text("".join(updated_lines), encoding="utf-8")


def reset_readme(file_path: Path) -> None:
    """Reset the README.md file's table, in order to add the new table to it."""
    lines = file_path.read_text(encoding="utf-8").splitlines()

    new_lines = []
    keep_table_header = False

    for line in lines:
        # Check if it's the table header or divider row
        if line.strip().startswith("| Name") or line.strip().startswith("| :"):
            keep_table_header = True
            new_lines.append(line)
            continue

        if keep_table_header and line.strip().startswith("|"):
            continue

        new_lines.append(line)

    file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def main():

    reset_readme(README_PATH)

    new_rows = generate_readme_table(ROOT_PATH)

    insert_rows_to_table(README_PATH, new_rows)


if __name__ == "__main__":
    main()
