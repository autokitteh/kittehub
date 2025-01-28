"""Extract metadata from project README files to update table in repo's README file."""

from pathlib import Path
import re


ROOT_PATH = Path(__file__).parent


def extract_metadata(readme_file: Path) -> dict:
    """Extract metadata from a project's README file."""
    field_pattern = r"^([a-z]+):\s+(.+)"  # "key: value"
    f = readme_file.read_text(encoding="utf-8")
    metadata = {}

    # These 2 metadata values are string lists, others are simple strings.
    list_values = ("categories", "integrations")

    for k, v in re.findall(field_pattern, f, re.MULTILINE):
        # Integrations and categories are a list of strings, others are just strings.
        if k in list_values:
            metadata[k] = re.findall(r'"(.+?)"', v)
        else:
            metadata[k] = v

    return metadata


def to_table_row(project_dir: Path, metadata: dict) -> str:
    """Convert metadata into a markdown table row."""
    title = metadata.get("title", "")
    if not title:
        return ""

    description = metadata.get("description", "")
    integrations = ", ".join(metadata.get("integrations", []))
    path = project_dir.relative_to(ROOT_PATH)

    return f"| [{title}](./{path}/) | {description} | {integrations} |\n"


def insert_rows_to_table(readme_file: Path, new_rows: list[str]) -> None:
    """Insert rows into the table section of the README file."""
    md = readme_file.read_text(encoding="utf-8")
    table = "-->\n| Name | Description | Integration |\n"
    table += "| :--- | :---------- | :---------- |\n"

    for row in new_rows:
        table += row

    md = re.sub("-->.+<!--", table + "<!--", md, flags=re.DOTALL)
    readme_file.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    rows = []
    for f in sorted(ROOT_PATH.rglob("README.md")):
        rows.append(to_table_row(f.parent, extract_metadata(f)))
    rows = [r for r in rows if r]  # Remove empty rows.

    insert_rows_to_table(ROOT_PATH / "README.md", rows)
