"""Extract metadata from project README files to update table in repo's README file."""

import os
from pathlib import Path
import re


BADGE_URL = os.getenv("BADGE_URL", "https://app.autokitteh.cloud/template?name=")
BADGE_ALT = os.getenv("BADGE_ALT", "Start with AutoKitteh")
BADGE_IMG = "https://autokitteh.com/assets/autokitteh-badge.svg"


DIRNAME_VALIDATOR = re.compile(r"^[a-zA-Z0-9_./-]+$")
ROOT_PATH = Path(__file__).parent
IGNORED_DIRS = [
    ROOT_PATH / "samples/discord",
    ROOT_PATH / "slack_discord_sync",
    ROOT_PATH / "discord_to_spreadsheet",
]


def extract_metadata(readme_file: Path) -> dict:
    """Extract metadata from a project's README file."""
    field_pattern = r"^([a-z]+):\s+(.+)"
    f = readme_file.read_text(encoding="utf-8")
    metadata = {}
    list_values = ("categories", "integrations")
    for k, v in re.findall(field_pattern, f, re.MULTILINE):
        v = v.strip()
        if k in list_values:
            v_stripped = v
            if v_stripped.startswith("[") and v_stripped.endswith("]"):
                metadata[k] = [
                    item.strip() for item in re.findall(r'"(.+?)"', v_stripped)
                ]
            else:
                metadata[k] = []
        else:
            metadata[k] = v
    return metadata


def is_metadata_complete(metadata: dict) -> bool:
    """Check if required metadata fields are present and non-empty."""
    required_keys = {"title", "description", "integrations", "categories"}
    for key in required_keys:
        value = metadata.get(key)
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, list) and not value:
            return False
    return True


def is_directory_complete(directory: Path) -> bool:
    """Check if directory is complete: has .py or autokitteh.yaml and complete metadata. If only README, that's okay. If missing one of .py/.yaml/metadata, error."""  # noqa: E501
    has_python_files = any(directory.glob("*.py"))
    has_autokitteh_yaml = (directory / "autokitteh.yaml").exists()
    readme_file = directory / "README.md"
    has_readme = readme_file.is_file()
    metadata = extract_metadata(readme_file) if has_readme else {}
    complete_metadata = is_metadata_complete(metadata)
    if has_python_files or has_autokitteh_yaml:
        if complete_metadata:
            return True
        else:
            raise ValueError(
                f"Directory '{directory}' contains code or YAML but has "
                "incomplete metadata in README.md."
            )
    elif has_readme and not (has_python_files or has_autokitteh_yaml):
        return False  # Only README is present, that's okay
    else:
        raise ValueError(
            f"Directory '{directory}' is missing required files "
            "(README.md, .py, or autokitteh.yaml)."
        )


def generate_badge_html(dir_name: str) -> str:
    """Generate HTML for the badge."""
    return f"[![{BADGE_ALT}]({BADGE_IMG})]({BADGE_URL}{dir_name})"


def generate_table_row(project_dir: Path, metadata: dict, root_path: Path) -> str:
    title = metadata.get("title", "").strip()
    if not title:
        return ""
    description = metadata.get("description", "").strip()
    integrations = ", ".join(metadata.get("integrations", []))
    path = project_dir.relative_to(root_path)
    dir_name_for_badge = project_dir.relative_to(root_path).as_posix()
    badge_html_for_table = generate_badge_html(dir_name_for_badge)
    return (
        f"| [{title}](./{path}/)<br/>{badge_html_for_table} | "
        f"{description} | {integrations} |\n"
    )


def generate_table(root_path: Path) -> list:
    rows = []
    errors = []
    for f in sorted(root_path.rglob("README.md")):
        if f.parent == root_path or any(
            f.parent.is_relative_to(ignored_dir) for ignored_dir in IGNORED_DIRS
        ):
            continue
        try:
            if is_directory_complete(f.parent):
                metadata = extract_metadata(f)
                row = generate_table_row(f.parent, metadata, root_path)
                if row.strip():
                    rows.append(row)
            else:
                # Only README present, skip
                continue
        except (OSError, ValueError) as e:
            errors.append(f"Directory '{f.parent}': {str(e)}")
            continue
    if rows:
        readme_file = root_path / "README.md"
        md = readme_file.read_text(encoding="utf-8")
        table = "-->\n| Name | Description | Integration |\n"
        table += "| :--- | :---------- | :---------- |\n"
        for row in rows:
            table += row
        md = re.sub("-->.+<!--", table + "<!--", md, flags=re.DOTALL)
        readme_file.write_text(md, encoding="utf-8")
    return rows, errors


if __name__ == "__main__":
    rows, errors = generate_table(ROOT_PATH)
    if errors:
        for err in errors:
            print(f"[ERROR] {err}")
