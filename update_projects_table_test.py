"""Unit tests for the "update_projects_table" module."""

from pathlib import Path
import re
from urllib.parse import urlparse

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

    def test_non_empty_categories_field(self, tmp_file):
        tmp_file.write_text('categories: ["a"]')
        expected = {"categories": ["a"]}
        assert update_projects_table.extract_metadata(tmp_file) == expected

        tmp_file.write_text('categories: ["a", "b"]')
        expected = {"categories": ["a", "b"]}
        assert update_projects_table.extract_metadata(tmp_file) == expected


class TestToTableRow:
    """Unit tests for the "to_table_row" function."""

    @pytest.fixture
    def test_paths(self, tmp_path):
        """Create test paths for the table row tests."""
        base_path = tmp_path
        project_dir = base_path / "dir"
        project_dir.mkdir(exist_ok=True)
        return base_path, project_dir

    def test_to_table_row(self, test_paths):
        base_path, project_dir = test_paths

        # Metadata without a title - ignore it.
        metadata = {"description": "d", "integrations": ["1"]}
        actual = update_projects_table.generate_table_row(
            project_dir, metadata, base_path
        )
        assert actual == ""

        # Metadata with nothing but the title.
        metadata = {"title": "blah blah blah"}
        actual = update_projects_table.generate_table_row(
            project_dir, metadata, base_path
        )
        expected = (
            "| [blah blah blah](./dir/)<br/>"
            f"[![{update_projects_table.BADGE_ALT}]({update_projects_table.BADGE_IMG})]"
            f"({update_projects_table.BADGE_URL}dir) |  |  |\n"
        )
        assert actual == expected

        # Regular project with a single integration.
        metadata = {"title": "t", "description": "d", "integrations": ["1"]}
        actual = update_projects_table.generate_table_row(
            project_dir, metadata, base_path
        )
        expected = (
            "| [t](./dir/)<br/>"
            f"[![{update_projects_table.BADGE_ALT}]({update_projects_table.BADGE_IMG})]"
            f"({update_projects_table.BADGE_URL}dir) | d | 1 |\n"
        )
        assert actual == expected

        # Regular project with multiple integrations.
        metadata = {"title": "t", "description": "d", "integrations": ["1", "2", "3"]}
        actual = update_projects_table.generate_table_row(
            project_dir, metadata, base_path
        )
        expected = (
            "| [t](./dir/)<br/>"
            f"[![{update_projects_table.BADGE_ALT}]({update_projects_table.BADGE_IMG})]"
            f"({update_projects_table.BADGE_URL}dir) | d | 1, 2, 3 |\n"
        )
        assert actual == expected


class TestInsertRowsToTable:
    """Unit tests for table generation in README."""

    @pytest.fixture
    def readme_file(self, tmp_path):
        """Create a temporary README file with table markers."""
        template = "prefix\n<!--start-table-->\ngarbage\n<!--end-table-->\nsuffix\n"
        fp = tmp_path / "README.md"
        fp.write_text(template)
        yield fp
        fp.unlink()

    def test_generate_table_empty(self, readme_file, monkeypatch):
        """Test generation of an empty table."""

        # Mock functions that would search the filesystem
        def mock_rglob(*args, **kwargs):
            return []

        monkeypatch.setattr(Path, "rglob", mock_rglob)

        # Run the function
        rows, errors = update_projects_table.generate_table(readme_file.parent)

        # Verify results
        assert len(rows) == 0
        assert len(errors) == 0

    def test_generate_table_with_rows(self, tmp_path, monkeypatch):
        """Test generation of table with actual content."""
        # Setup directory structure
        root = tmp_path
        readme = root / "README.md"
        readme_content = (
            "prefix\n<!--start-table-->\nold content\n<!--end-table-->\nsuffix\n"
        )
        readme.write_text(readme_content)

        # Create a project directory with complete metadata
        project_dir = root / "project1"
        project_dir.mkdir()
        project_readme = project_dir / "README.md"
        metadata_content = (
            "title: Test Project\n"
            "description: Test Description\n"
            'integrations: ["test"]\n'
            'categories: ["test"]'
        )
        project_readme.write_text(metadata_content)
        (project_dir / "test.py").write_text("# Test file")

        # Mock is_directory_complete to always return True
        monkeypatch.setattr(
            update_projects_table, "is_directory_complete", lambda x: True
        )

        # Run the function
        rows, errors = update_projects_table.generate_table(root)

        # Verify results
        assert len(rows) == 1
        assert "Test Project" in rows[0]
        assert len(errors) == 0

        # Check that the README was updated
        content = readme.read_text()
        assert "Test Project" in content
        assert "old content" not in content

    def test_generate_table_with_error(self, tmp_path, monkeypatch):
        """Test handling of errors during table generation."""
        # Setup directory structure
        root = tmp_path
        readme = root / "README.md"
        readme.write_text("prefix\n<!--start-table-->\n<!--end-table-->\nsuffix\n")

        # Create project directory that will generate an error
        project_dir = root / "error_project"
        project_dir.mkdir()
        (project_dir / "README.md").write_text("# Incomplete metadata")

        # Mock is_directory_complete to raise an error
        def mock_is_directory_complete(path):
            raise ValueError("Test error")

        monkeypatch.setattr(
            update_projects_table, "is_directory_complete", mock_is_directory_complete
        )

        # Run the function
        rows, errors = update_projects_table.generate_table(root)

        # Verify error was captured
        assert len(rows) == 0
        assert len(errors) == 1
        assert "Test error" in errors[0]


class TestValidateUrls:
    """Tests to validate that URLs in the module are properly formatted."""

    def test_badge_url_is_valid(self):
        """Test that BADGE_URL is a valid URL."""
        url = update_projects_table.BADGE_URL
        # Check if it's a URL with proper scheme
        parsed = urlparse(url)
        assert parsed.scheme in ("http", "https"), f"Invalid URL scheme: {url}"
        assert parsed.netloc, f"Missing domain in URL: {url}"

        # Verify it ends with a parameter name
        assert re.search(r"\?.*=.*$", url), "URL missing query parameter format"

    def test_badge_img_is_valid(self):
        """Test that BADGE_IMG is a valid image URL."""
        url = update_projects_table.BADGE_IMG
        # Check if it's a URL with proper scheme
        parsed = urlparse(url)
        assert parsed.scheme in ("http", "https"), f"Invalid URL scheme: {url}"
        assert parsed.netloc, f"Missing domain in URL: {url}"

        # Verify it points to an image
        assert parsed.path.endswith((".svg", ".png", ".jpg", ".jpeg", ".gif")), (
            f"URL does not point to a recognized image format: {url}"
        )


class TestMetadataValidation:
    """Tests for metadata validation functions."""

    def test_is_metadata_complete_success(self):
        """Test that complete metadata passes validation."""
        metadata = {
            "title": "Test Project",
            "description": "A test project",
            "integrations": ["test1", "test2"],
            "categories": ["cat1", "cat2"],
        }
        assert update_projects_table.is_metadata_complete(metadata) is True

    def test_is_metadata_complete_missing_field(self):
        """Test that metadata with missing fields fails validation."""
        # Missing title
        metadata = {
            "description": "A test project",
            "integrations": ["test1", "test2"],
            "categories": ["cat1", "cat2"],
        }
        assert update_projects_table.is_metadata_complete(metadata) is False

        # Missing description
        metadata = {
            "title": "Test Project",
            "integrations": ["test1", "test2"],
            "categories": ["cat1", "cat2"],
        }
        assert update_projects_table.is_metadata_complete(metadata) is False

        # Missing integrations
        metadata = {
            "title": "Test Project",
            "description": "A test project",
            "categories": ["cat1", "cat2"],
        }
        assert update_projects_table.is_metadata_complete(metadata) is False

        # Missing categories
        metadata = {
            "title": "Test Project",
            "description": "A test project",
            "integrations": ["test1", "test2"],
        }
        assert update_projects_table.is_metadata_complete(metadata) is False

    def test_is_metadata_complete_empty_values(self):
        """Test that metadata with empty values fails validation."""
        # Empty title
        metadata = {
            "title": "",
            "description": "A test project",
            "integrations": ["test1", "test2"],
            "categories": ["cat1", "cat2"],
        }
        assert update_projects_table.is_metadata_complete(metadata) is False

        # Empty description
        metadata = {
            "title": "Test Project",
            "description": "",
            "integrations": ["test1", "test2"],
            "categories": ["cat1", "cat2"],
        }
        assert update_projects_table.is_metadata_complete(metadata) is False

        # Empty integrations
        metadata = {
            "title": "Test Project",
            "description": "A test project",
            "integrations": [],
            "categories": ["cat1", "cat2"],
        }
        assert update_projects_table.is_metadata_complete(metadata) is False

        # Empty categories
        metadata = {
            "title": "Test Project",
            "description": "A test project",
            "integrations": ["test1", "test2"],
            "categories": [],
        }
        assert update_projects_table.is_metadata_complete(metadata) is False


class TestDirectoryValidation:
    """Tests for directory validation functions."""

    @pytest.fixture
    def setup_directory(self, tmp_path):
        """Set up a directory with various configurations for testing."""
        base_dir = tmp_path

        # Complete directory with Python file and metadata
        complete_dir = base_dir / "complete"
        complete_dir.mkdir()
        (complete_dir / "test.py").write_text("# Test file")
        complete_readme = complete_dir / "README.md"
        complete_readme.write_text(
            "title: Complete\n"
            "description: Complete description\n"
            'integrations: ["int1"]\n'
            'categories: ["cat1"]\n'
        )

        # Directory with Python file but incomplete metadata
        incomplete_dir = base_dir / "incomplete"
        incomplete_dir.mkdir()
        (incomplete_dir / "test.py").write_text("# Test file")
        incomplete_readme = incomplete_dir / "README.md"
        incomplete_readme.write_text("title: Incomplete\n")

        # Directory with only README (no code)
        readme_only_dir = base_dir / "readme_only"
        readme_only_dir.mkdir()
        readme_only = readme_only_dir / "README.md"
        readme_only.write_text(
            "title: README Only\n"
            "description: Just a README\n"
            'integrations: ["int1"]\n'
            'categories: ["cat1"]\n'
        )

        # Directory with yaml file
        yaml_dir = base_dir / "yaml_dir"
        yaml_dir.mkdir()
        (yaml_dir / "autokitteh.yaml").write_text("# YAML file")
        yaml_readme = yaml_dir / "README.md"
        yaml_readme.write_text(
            "title: YAML Project\n"
            "description: YAML description\n"
            'integrations: ["int1"]\n'
            'categories: ["cat1"]\n'
        )

        # Directory with no files
        empty_dir = base_dir / "empty"
        empty_dir.mkdir()

        return base_dir

    def test_is_directory_complete_success(self, setup_directory):
        """Test successful directory validation."""
        complete_dir = setup_directory / "complete"
        assert update_projects_table.is_directory_complete(complete_dir) is True

        yaml_dir = setup_directory / "yaml_dir"
        assert update_projects_table.is_directory_complete(yaml_dir) is True

    def test_is_directory_complete_readme_only(self, setup_directory):
        """Test directory with only README."""
        readme_only_dir = setup_directory / "readme_only"
        assert update_projects_table.is_directory_complete(readme_only_dir) is False

    def test_is_directory_complete_errors(self, setup_directory):
        """Test directories that should raise errors."""
        incomplete_dir = setup_directory / "incomplete"
        with pytest.raises(ValueError, match=r".*incomplete metadata.*"):
            update_projects_table.is_directory_complete(incomplete_dir)

        empty_dir = setup_directory / "empty"
        with pytest.raises(ValueError, match=r".*missing required files.*"):
            update_projects_table.is_directory_complete(empty_dir)


class TestBadgeGeneration:
    """Tests for badge HTML generation."""

    def test_generate_badge_html(self):
        """Test that badge HTML is correctly generated."""
        dir_name = "test_dir"
        badge_html = update_projects_table.generate_badge_html(dir_name)

        # Check that the HTML contains all the expected components
        assert update_projects_table.BADGE_ALT in badge_html
        assert update_projects_table.BADGE_IMG in badge_html
        assert f"{update_projects_table.BADGE_URL}{dir_name}" in badge_html

        # Check for proper markdown image link format
        assert badge_html.startswith("[![")
        assert "](" in badge_html
        assert ")](" in badge_html
        assert badge_html.endswith(")")
