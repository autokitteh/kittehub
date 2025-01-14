"""Unit tests for the "update_projects_table" module."""

from pathlib import Path

import pytest
import update_projects_table


class TestExtractMetadata:
    """Unit tests for the "extract_metadata" function."""

    @pytest.fixture
    def tmp_file(self, tmp_path):
        """Thin wrapper over "tmp_path" to create and delete a temporary file."""
        fp = tmp_path / "tmp_file"
        yield fp
        fp.unlink()

    def test_empty_metadata(self, tmp_file):
        tmp_file.write_text("")
        assert update_projects_table.extract_metadata(tmp_file) == {}

    def test_single_basic_field(self, tmp_file):
        tmp_file.write_text("foo: bar")
        assert update_projects_table.extract_metadata(tmp_file) == {"foo": "bar"}

    def test_single_basic_field_with_extra_whitespaces(self, tmp_file):
        tmp_file.write_text("foo:   bar\n\n\n")
        assert update_projects_table.extract_metadata(tmp_file) == {"foo": "bar"}

    def test_multiple_basic_fields(self, tmp_file):
        tmp_file.write_text("aaa: 111\nbbb: 222\nccc: 333\n")
        expected = {"aaa": "111", "bbb": "222", "ccc": "333"}
        assert update_projects_table.extract_metadata(tmp_file) == expected

    def test_empty_integrations_field(self, tmp_file):
        tmp_file.write_text("integrations:")
        assert update_projects_table.extract_metadata(tmp_file) == {}

        tmp_file.write_text("integrations: ")
        assert update_projects_table.extract_metadata(tmp_file) == {}

        tmp_file.write_text("integrations: []")
        assert update_projects_table.extract_metadata(tmp_file) == {"integrations": []}

    def test_non_empty_integrations_field(self, tmp_file):
        tmp_file.write_text('integrations: ["a"]')
        expected = {"integrations": ["a"]}
        assert update_projects_table.extract_metadata(tmp_file) == expected

        tmp_file.write_text('integrations: ["a",]')
        expected = {"integrations": ["a"]}
        assert update_projects_table.extract_metadata(tmp_file) == expected

        tmp_file.write_text('integrations: ["a","b"]')
        expected = {"integrations": ["a", "b"]}
        assert update_projects_table.extract_metadata(tmp_file) == expected

        tmp_file.write_text('integrations: ["a", "b"]')
        expected = {"integrations": ["a", "b"]}
        assert update_projects_table.extract_metadata(tmp_file) == expected

        tmp_file.write_text('integrations: ["a",  "b"]')
        expected = {"integrations": ["a", "b"]}
        assert update_projects_table.extract_metadata(tmp_file) == expected

    def test_combination_of_basic_and_integrations_fields(self, tmp_file):
        tmp_file.write_text('a: 1\nb: 2\nintegrations: ["c", "d"]\ne: 3')
        expected = {"a": "1", "b": "2", "integrations": ["c", "d"], "e": "3"}
        assert update_projects_table.extract_metadata(tmp_file) == expected


class TestToTableRow:
    """Unit tests for the "to_table_row" function."""

    def test_to_table_row(self):
        # Metadata without a title - ignore it.
        metadata = {"description": "d", "integrations": ["1"]}
        actual = update_projects_table.to_table_row(Path("dir").absolute(), metadata)
        assert actual == ""

        # Metadata with nothing but the title.
        metadata = {"title": "blah blah blah"}
        actual = update_projects_table.to_table_row(Path("dir").absolute(), metadata)
        assert actual == "| [blah blah blah](./dir/) |  |  |\n"

        # Regular project with a single integration.
        metadata = {"title": "t", "description": "d", "integrations": ["1"]}
        actual = update_projects_table.to_table_row(Path("dir").absolute(), metadata)
        assert actual == "| [t](./dir/) | d | 1 |\n"

        # Regular project with multiple integrations.
        metadata = {"title": "t", "description": "d", "integrations": ["1", "2", "3"]}
        actual = update_projects_table.to_table_row(Path("dir").absolute(), metadata)
        assert actual == "| [t](./dir/) | d | 1, 2, 3 |\n"


class TestInsertRowsToTable:
    """Unit tests for the "insert_rows_to_table" function."""

    @pytest.fixture
    def tmp_file(self, tmp_path):
        template = "prefix\n<!--start-table-->\ngarbage\n<!--end-table-->\nsuffix\n"
        fp = tmp_path / "tmp_file"
        fp.write_text(template)
        yield fp
        fp.unlink()

    def test_insert_rows_to_table_empty(self, tmp_file):
        update_projects_table.insert_rows_to_table(tmp_file, ["| row |\n"] * 0)
        assert tmp_file.read_text() == (
            "prefix\n<!--start-table-->\n"
            "| Name | Description | Integration |\n"
            "| :--- | :---------- | :---------- |\n"
            "<!--end-table-->\nsuffix\n"
        )

    def test_insert_rows_to_table_one_row(self, tmp_file):
        update_projects_table.insert_rows_to_table(tmp_file, ["| row |\n"] * 1)
        assert tmp_file.read_text() == (
            "prefix\n<!--start-table-->\n"
            "| Name | Description | Integration |\n"
            "| :--- | :---------- | :---------- |\n"
            "| row |\n"
            "<!--end-table-->\nsuffix\n"
        )

    def test_insert_rows_to_table_multiple_rows(self, tmp_file):
        update_projects_table.insert_rows_to_table(tmp_file, ["| row |\n"] * 3)
        assert tmp_file.read_text() == (
            "prefix\n<!--start-table-->\n"
            "| Name | Description | Integration |\n"
            "| :--- | :---------- | :---------- |\n"
            "| row |\n"
            "| row |\n"
            "| row |\n"
            "<!--end-table-->\nsuffix\n"
        )
