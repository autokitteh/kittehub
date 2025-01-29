"""Unit tests for the metadata block in project README files."""

from pathlib import Path
import sys

import pytest


sys.path.append(str(Path(__file__).resolve().parent.parent))


import update_projects_table

import metadata_definitions


ROOT_PATH = Path(__file__).parent.parent


def get_metadata_files(base_path=ROOT_PATH):
    """Helper function to yield README files and their metadata."""
    for readme_file in sorted(Path(base_path).rglob("README.md")):
        metadata = update_projects_table.extract_metadata(readme_file)
        if metadata:
            yield readme_file, metadata


def test_metadata_contains_all_fields():
    for readme_file, metadata in get_metadata_files():
        error = f"Metadata missing in README file: {readme_file}"
        assert all(key in metadata for key in metadata_definitions.METADATA), error


def test_metadtata_contains_at_least_1_integration():
    for readme_file, metadata in get_metadata_files():
        error = f"Metadata must have at least one integration: {readme_file}"
        assert metadata["integrations"], error


def test_metadtata_contains_at_least_1_category():
    for readme_file, metadata in get_metadata_files():
        error = f"Metadata must have at least one category: {readme_file}"
        assert metadata["categories"], error


METADATA_VALID = [
    (metadata_definitions.ALLOWED_CATEGORIES, "categories"),
    (metadata_definitions.ALLOWED_INTEGRATIONS, "integrations"),
]


@pytest.mark.parametrize(("allow_list", "metadata_type"), METADATA_VALID)
def test_metadata_have_only_allowed_values(allow_list, metadata_type):
    for readme_file, metadata in get_metadata_files():
        for item in metadata[metadata_type]:
            error = f"Invalid '{item}' in {metadata_type}: {readme_file}"
            assert item in allow_list, error


TEST_CATEGORIES = [
    (Path(ROOT_PATH / "devops"), "DevOps"),
    (Path(ROOT_PATH / "reliability"), "Reliability"),
    (Path(ROOT_PATH / "samples"), "Samples"),
]


@pytest.mark.parametrize(("folder_path", "category"), TEST_CATEGORIES)
def test_projects_include_required_category(folder_path, category):
    for readme_file, metadata in get_metadata_files(folder_path):
        error = f"Metadata is missing the {category!r} category: {readme_file}"
        assert category in metadata["categories"], error


def test_sample_projects_have_correct_title_format():
    for readme_file, metadata in get_metadata_files(ROOT_PATH / "samples"):
        error = f"Sample projects must have 'sample' in the title: {readme_file}"
        assert metadata["title"].endswith(" sample"), error
