"""Unit tests for the metadata block in project README files."""

from pathlib import Path

import update_projects_table

import metadata_definitions
import pytest


ROOT_PATH = Path(__file__).parent.parent

TEST_CATEGORIES = [
    (Path(ROOT_PATH / "devops"), "DevOps"),
    (Path(ROOT_PATH / "reliability"), "Reliability"),
    (Path(ROOT_PATH / "samples"), "Samples"),
]

METADATA_VALID = [
    (metadata_definitions.CATEGORIES, "categories"),
    (metadata_definitions.INTEGRATIONS, "integrations"),
]


def test_metadata_block_exists():
    """Checks for required metadata in README files."""
    for readme_file in sorted(Path(ROOT_PATH).rglob("README.md")):
        metadata = update_projects_table.extract_metadata(readme_file)

        assert metadata, f"Metadata block is missing in the README file: {readme_file}"
        assert all(key in metadata for key in metadata_definitions.METADATA), (
            f"{metadata['title']} metadata missing required fields."
        )
        assert metadata["integrations"], (
            f"{metadata['title']} metadata must have at least one integration."
        )
        assert metadata["categories"], (
            f"{metadata['title']} metadata must have at least one category."
        )


@pytest.mark.parametrize(("allow_list", "metadata_type"), METADATA_VALID)
def test_metadata_valid(allow_list, metadata_type):
    """Checks that metadata fields contain only allowed values."""
    for readme_file in sorted(Path(ROOT_PATH).rglob("README.md")):
        metadata = update_projects_table.extract_metadata(readme_file)

        if metadata:
            for item in metadata[metadata_type]:
                assert item in allow_list, (
                    f"Invalid '{item}' in {metadata_type} in {metadata['title']}."
                )


@pytest.mark.parametrize(("folder_path", "categorie"), TEST_CATEGORIES)
def test_required_categorie(folder_path, categorie):
    """Ensures projects in each folder include the required category."""
    for readme_file in sorted(folder_path.rglob("README.md")):
        metadata = update_projects_table.extract_metadata(readme_file)

        if metadata:
            message = f"{metadata['title']} Project in /{categorie}"
            message += f" is missing the {categorie} categorie."
            assert categorie in metadata["categories"], message


def test_sample_name():
    for readme_file in sorted(Path(ROOT_PATH / "samples").rglob("README.md")):
        metadata = update_projects_table.extract_metadata(readme_file)

        if metadata:
            assert "sample" in metadata["title"], (
                "Sample projects must have the word 'sample' in the title."
            )
