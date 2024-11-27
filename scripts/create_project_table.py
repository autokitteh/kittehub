import os
import glob
import yaml
from typing import List

FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../README.md")


class ReadmeMetadataProcessor:
    def __init__(self, readme_file):
        self.readme_file = readme_file
        self.metadata = self.extract_metadata()

    def extract_metadata(self) -> dict:
        metadata = {}
        with open(self.readme_file, "r") as file:
            lines = file.readlines()

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
        relative_path = os.path.relpath(os.path.dirname(self.readme_file), FOLDER_PATH)
        link = f"./{relative_path}/"

        return f"| [{title}]({link}) | {description} | {integrations} |\n"


def generate_readme_table(folder_path) -> List[str]:
    """Generate a list of table rows from README metadata."""
    readme_files = glob.glob(
        os.path.join(folder_path, "**", "README.md"), recursive=True
    )

    rows = []
    for readme_file in readme_files:
        processor = ReadmeMetadataProcessor(readme_file)
        row = processor.to_table_row()
        if row:
            rows.append(row)
    return rows


def insert_rows_to_table_start(readme_file, new_rows) -> None:
    with open(readme_file, "r") as file:
        lines = file.readlines()

    try:
        header_index = (
            next(
                i
                for i, line in enumerate(lines)
                if line.startswith("| Name") and "| Description" in line
            )
            + 2
        )
    except StopIteration:
        print("No table header found.")
        return

    lines[header_index:header_index] = new_rows

    with open(readme_file, "w") as file:
        file.writelines(lines)


def process_readme(file_path) -> None:
    """
    Clean the README file by removing old table rows while keeping the header.

    This prepares the README for a new table to be added.
    """
    new_lines = []
    keep_table_header = False

    with open(file_path, "r") as file:
        for line in file:
            # Check if it's the table header or divider row
            if line.strip().startswith("| Name") or line.strip().startswith("| :"):
                keep_table_header = True
                new_lines.append(line)
                continue

            if keep_table_header and line.strip().startswith("|"):
                continue

            new_lines.append(line)

    with open(file_path, "w") as file:
        file.writelines(new_lines)


def main():
    print("Starting README processing...")
    process_readme(OUTPUT_PATH)
    print("Cleaned up existing table in README.")

    new_rows = generate_readme_table(FOLDER_PATH)
    print(f"Generated {len(new_rows)} new table rows.")

    if new_rows:
        insert_rows_to_table_start(OUTPUT_PATH, new_rows)
        print(f"Inserted {len(new_rows)} rows into the table in {OUTPUT_PATH}.")
    else:
        print("No new rows to insert.")

    print("README table update completed.")


if __name__ == "__main__":
    main()
