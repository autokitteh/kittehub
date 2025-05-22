"""Tests for README badge conventions in project READMEs."""

from pathlib import Path
import sys


sys.path.append(str(Path(__file__).resolve().parent.parent))

# Constants for badge validation
EXPECTED_BADGE_ALT_TEXT = "Start with AutoKitteh"
EXPECTED_BADGE_SVG_URL = "https://autokitteh.com/assets/autokitteh-badge.svg"
EXPECTED_BADGE_LINK_URL_PREFIX = "https://app.autokitteh.cloud/template?name="

# Directories to ignore when scanning for READMEs
IGNORED_DIRS_ANY_PART = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "target",
    "out",
    ".vscode",
    ".idea",
}

# Root path of the repository
ROOT_PATH = Path(__file__).parent.parent


def get_all_readme_files(base_path: Path):
    """Yields README.md files that should be checked for the standard project badge.

    Skips:
    - The root README.md file.
    - READMEs in universally ignored directories (like .git, node_modules).
      if they are configured to be skipped.
    """
    for readme_file in sorted(base_path.rglob("README.md")):
        if readme_file == base_path / "README.md":  # Skip root README
            continue

        relative_path = readme_file.relative_to(base_path)

        # Skip if any part of the path is in IGNORED_DIRS_ANY_PART
        if any(part in IGNORED_DIRS_ANY_PART for part in relative_path.parts):
            continue

        yield readme_file


def test_readme_has_correct_badge():
    """Tests that relevant README files contain the correct autokitteh badge.

    The badge must link to the project's directory name and use the standard SVG.
    Example: For ai-chat-assistant/README.md, the link must be
    https://app.autokitteh.cloud/template?name=ai-chat-assistant
    The image URL must be https://autokitteh.com/assets/autokitteh-badge.svg
    """
    errors = []
    for readme_file in get_all_readme_files(ROOT_PATH):
        try:
            # dir_name is the relative path of the README's parent directory
            # from ROOT_PATH, e.g., "ai-chat-assistant" or "devops/purrr"
            dir_name = readme_file.parent.relative_to(ROOT_PATH).as_posix()

            if not dir_name or dir_name == ".":
                errors.append(
                    f"README file: {readme_file.relative_to(ROOT_PATH)}\n"
                    "  Could not determine a valid directory name for the badge link."
                )
                continue

            expected_link_url = EXPECTED_BADGE_LINK_URL_PREFIX + dir_name
            expected_badge_markdown = (
                f"[![{EXPECTED_BADGE_ALT_TEXT}]({EXPECTED_BADGE_SVG_URL})]"
                f"({expected_link_url})"
            )

            content = readme_file.read_text(encoding="utf-8")
            if expected_badge_markdown not in content:
                errors.append(
                    f"README file: {readme_file.relative_to(ROOT_PATH)}\n"
                    "  Missing or incorrect badge.\n"
                    f"  Expected: {expected_badge_markdown}\n"
                )
        except FileNotFoundError:
            errors.append(
                f"README file not found (unexpected): "
                f"{readme_file.relative_to(ROOT_PATH)}"
            )
        except UnicodeDecodeError:
            errors.append(
                f"README file: {readme_file.relative_to(ROOT_PATH)}\n"
                "  Could not be read as UTF-8."
            )
        except Exception as e:  # noqa: BLE001
            errors.append(
                f"Error processing file {readme_file.relative_to(ROOT_PATH)}: "
                f"{type(e).__name__} - {e}"
            )

    assert not errors, "README badge convention errors found:\n\n" + "\n".join(errors)
