from pathlib import Path
import tempfile
import unittest

import update_projects_table


class TestCreateProjectTable(unittest.TestCase):
    """Unit tests for the "update_projects_table" module."""

    def generic_test_extract_metadata(self, input, expected):
        actual = {}
        with tempfile.NamedTemporaryFile(delete_on_close=False) as f:
            if input:
                f.write(input)
            f.close()
            actual = update_projects_table.extract_metadata(Path(f.name))
        self.assertEqual(expected, actual)

    def test_extract_metadata(self):
        # Empty metadata.
        self.generic_test_extract_metadata(None, {})

        # Single basic field.
        self.generic_test_extract_metadata(b"foo: bar", {"foo": "bar"})

        # Single basic field with extra whitespaces (a recoverable typo).
        self.generic_test_extract_metadata(b"foo:   bar\n\n\n", {"foo": "bar"})

        # Multiple basic fields.
        input = b"aaa: 111\nbbb: 222\nccc: 333\n"
        expected = {"aaa": "111", "bbb": "222", "ccc": "333"}
        self.generic_test_extract_metadata(input, expected)

        # Empty integrations field.
        self.generic_test_extract_metadata(b"integrations:", {})
        self.generic_test_extract_metadata(b"integrations: ", {})
        self.generic_test_extract_metadata(b"integrations: []", {"integrations": []})

        # Non-empty integrations field.
        input = b'integrations: ["a"]'
        expected = {"integrations": ["a"]}
        self.generic_test_extract_metadata(input, expected)

        input = b'integrations: ["a",]'
        expected = {"integrations": ["a"]}
        self.generic_test_extract_metadata(input, expected)

        input = b'integrations: ["a","b"]'
        expected = {"integrations": ["a", "b"]}
        self.generic_test_extract_metadata(input, expected)

        input = b'integrations: ["a", "b"]'
        expected = {"integrations": ["a", "b"]}
        self.generic_test_extract_metadata(input, expected)

        # Combination of basic and integrations fields.
        input = b'a: 1\nb: 2\nintegrations: ["c", "d"]\ne: 3'
        expected = {"a": "1", "b": "2", "integrations": ["c", "d"], "e": "3"}
        self.generic_test_extract_metadata(input, expected)

    def test_to_table_row(self):
        # Metadata without a title - ignore it.
        metadata = {"description": "d", "integrations": ["1"]}
        actual = update_projects_table.to_table_row(Path("dir").absolute(), metadata)
        self.assertEqual("", actual)

        # Metadata with nothing but the title.
        metadata = {"title": "blah blah blah"}
        expected = "| [blah blah blah](./dir/) |  |  |\n"
        actual = update_projects_table.to_table_row(Path("dir").absolute(), metadata)
        self.assertEqual(expected, actual)

        # Regular project with a single integration.
        metadata = {"title": "t", "description": "d", "integrations": ["1"]}
        expected = "| [t](./dir/) | d | 1 |\n"
        actual = update_projects_table.to_table_row(Path("dir").absolute(), metadata)
        self.assertEqual(expected, actual)

        # Regular project with multiple integrations.
        metadata = {"title": "t", "description": "d", "integrations": ["1", "2", "3"]}
        expected = "| [t](./dir/) | d | 1, 2, 3 |\n"
        actual = update_projects_table.to_table_row(Path("dir").absolute(), metadata)
        self.assertEqual(expected, actual)

    def generic_test_insert_rows_to_table(self, num_rows, expected):
        actual = ""
        with tempfile.NamedTemporaryFile(delete_on_close=False) as f:
            f.write(b"prefix\n<!--start-table-->\ngarbage\n<!--end-table-->\nsuffix\n")
            f.close()
            rows = ["| row |\n"] * num_rows
            update_projects_table.insert_rows_to_table(Path(f.name), rows)
            actual = Path(f.name).read_text()
        self.assertEqual(expected, actual)

    def test_insert_rows_to_table_empty(self):
        expected = (
            "prefix\n<!--start-table-->\n"
            "| Name | Description | Integration |\n"
            "| :--- | :---------- | :---------- |\n"
            "<!--end-table-->\nsuffix\n"
        )
        self.generic_test_insert_rows_to_table(0, expected)

    def test_insert_rows_to_table_one_row(self):
        expected = (
            "prefix\n<!--start-table-->\n"
            "| Name | Description | Integration |\n"
            "| :--- | :---------- | :---------- |\n"
            "| row |\n"
            "<!--end-table-->\nsuffix\n"
        )
        self.generic_test_insert_rows_to_table(1, expected)

    def test_insert_rows_to_table_multiple_rows(self):
        expected = (
            "prefix\n<!--start-table-->\n"
            "| Name | Description | Integration |\n"
            "| :--- | :---------- | :---------- |\n"
            "| row |\n"
            "| row |\n"
            "| row |\n"
            "<!--end-table-->\nsuffix\n"
        )
        self.generic_test_insert_rows_to_table(3, expected)


if __name__ == "__main__":
    unittest.main()
