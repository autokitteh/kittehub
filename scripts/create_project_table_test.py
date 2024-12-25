import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import create_project_table


class TestCreateProjectTable(unittest.TestCase):

    def test_extract_metadata(self):
        # Define the content to be written to the temporary file
        readme_content = """\
Header text

title: Example Project
description: An example project for testing.
integrations: "slack", "gemini"

Other notes
"""
        expected_metadata = {
            "title": "Example Project",
            "description": "An example project for testing.",
            "integrations": ["slack", "gemini"],
        }

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            temp_file_path = Path(temp_file.name)
            temp_file.write(readme_content)
            temp_file.flush()
        try:
            metadata = create_project_table.extract_metadata(temp_file_path)
            self.assertEqual(metadata, expected_metadata)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def test_extract_metadata_missing_fields(self):
        readme_content = """\
title: Example Project
description: An example project for testing.
"""
        expected_metadata = {
            "title": "Example Project",
            "description": "An example project for testing.",
        }

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            temp_file_path = Path(temp_file.name)
            temp_file.write(readme_content)
            temp_file.flush()
        try:
            metadata = create_project_table.extract_metadata(temp_file_path)
            self.assertEqual(metadata, expected_metadata)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def test_extract_metadata_empty_file(self):
        readme_content = ""

        expected_metadata = {}

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            temp_file_path = Path(temp_file.name)
            temp_file.write(readme_content)
            temp_file.flush()
        try:
            metadata = create_project_table.extract_metadata(temp_file_path)
            self.assertEqual(metadata, expected_metadata)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

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

    def test_generate_readme_table(self):
        readme_content = """\
Header text      

title: Example Project
description: An example project for testing.
integrations: "slack", "gemini"

Other notes
"""

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            temp_file_path = temp_dir_path / "README.md"

            with temp_file_path.open(mode="w", encoding="utf-8") as temp_file:
                temp_file.write(readme_content)
                temp_file.flush()

            relative_path = os.path.relpath(
                temp_dir_path, create_project_table.ROOT_PATH
            )
            expected_row = [
                f"| [Example Project](./{relative_path}/) | An example project for testing. | slack, gemini |\n"
            ]

            rows = create_project_table.generate_readme_table(temp_dir_path)
            self.assertEqual(rows, expected_row)

    def test_generate_readme_table_empty_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            rows = create_project_table.generate_readme_table(temp_dir_path)
            self.assertEqual(rows, [])

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
