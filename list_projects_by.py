"""Enumerate projects by category/integration, based on their README metadata."""

import collections
import sys

from update_projects_table import extract_metadata
from update_projects_table import ROOT_PATH


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("categories", "integrations"):
        print(f"Usage: {sys.argv[0]} <categories|integrations>")
        sys.exit(1)

    label = sys.argv[1]
    data = collections.defaultdict(list)

    # Extract metadata from README files and group by category/integration.
    for readme_file in sorted(ROOT_PATH.rglob("README.md")):
        metadata = extract_metadata(readme_file)
        metadata["path"] = readme_file.parent.relative_to(ROOT_PATH)
        for key in metadata.get(label, []):
            data[key].append(metadata)

    # Print all the projects associated with each category/integration.
    for key, projects in sorted(data.items()):
        print(f"{key}: {len(projects)}")
        for project in sorted(projects, key=lambda p: p["title"]):
            print(f"    {project['title']} -- /{project['path']}")
        print()
