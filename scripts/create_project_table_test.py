from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch
import create_project_table


class TestCreateProjectTable(unittest.TestCase):

    def test_extract_metadata(self):
        mock_readme_content = """\
title: Example Project
description: An example project for testing.
integrations: "slack", "gemini"
extra_key: This should not appear
"""

        mock_readme_file = MagicMock()
        mock_readme_file.read_text.return_value = mock_readme_content

        expected_metadata = {
            "title": "Example Project",
            "description": "An example project for testing.",
            "integrations": ["slack", "gemini"],
        }

        metadata = create_project_table.extract_metadata(mock_readme_file)
        self.assertEqual(metadata, expected_metadata)

    def test_to_table_row(self):
        mock_readme_file = Path("./projects/project1/README.md")

        metadata = {
            "title": "Project One",
            "description": "An example project for testing.",
            "integrations": ["slack", "gemini"],
        }

        expected_row = "| [Project One](./projects/project1/) | An example project for testing. | slack, gemini |\n"
        row = create_project_table.to_table_row(mock_readme_file, metadata)
        self.assertEqual(row, expected_row)

    @patch("create_project_table.Path.rglob")
    @patch("create_project_table.extract_metadata")
    @patch("create_project_table.to_table_row")
    def test_generate_readme_table(
        self, mock_to_table_row, mock_extract_metadata, mock_rglob
    ):
        # Mock the README files found by rglob
        mock_readme_file = MagicMock(spec=Path)
        mock_readme_file.parent = Path("./mock/project")
        mock_rglob.return_value = [mock_readme_file]

        mock_extract_metadata.return_value = {
            "title": "Example Project",
            "description": "An example project for testing.",
            "integrations": ["slack", "gemini"],
        }

        mock_to_table_row.return_value = "| [Example Project](./mock/project/) | An example project for testing. | slack, gemini |\n"

        expected_rows = [
            "| [Example Project](./mock/project/) | An example project for testing. | slack, gemini |\n"
        ]

        # Test the function
        rows = create_project_table.generate_readme_table(Path("/mock"))
        self.assertEqual(rows, expected_rows)

        mock_rglob.assert_called_once_with("README.md")
        mock_extract_metadata.assert_called_once_with(mock_readme_file)
        mock_to_table_row.assert_called_once_with(
            mock_readme_file, mock_extract_metadata.return_value
        )

    def test_insert_rows_to_table(self):
        mock_readme_content = """\
# Example README

Some introductory text.

<!--start-table-->
| Name | Description | Integration |
| :--- | :---------- | :---------- |
<!--end-table-->

Some footer text.
"""

        expected_readme_content = """\
# Example README

Some introductory text.

<!--start-table-->
| Name | Description | Integration |
| :--- | :---------- | :---------- |
| [Project One](./project1/) | Example project one. | slack |
| [Project Two](./project2/) | Example project two. | gemini |
<!--end-table-->

Some footer text.
"""

        new_rows = [
            "| [Project One](./project1/) | Example project one. | slack |\n",
            "| [Project Two](./project2/) | Example project two. | gemini |\n",
        ]

        mock_readme_file = MagicMock(spec=Path)

        mock_readme_file.read_text.return_value = mock_readme_content
        mock_readme_file.write_text = MagicMock()

        create_project_table.insert_rows_to_table(mock_readme_file, new_rows)

        mock_readme_file.write_text.assert_called_once_with(
            expected_readme_content, encoding="utf-8"
        )

        mock_readme_file.read_text.assert_called_once_with(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
