"""Enumerate projects by category/integration, based on their README metadata."""

import collections
import sys

from update_projects_table import extract_metadata
from update_projects_table import ROOT_PATH


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("category", "integration"):
        print(f"Usage: {sys.argv[0]} <category|integration>")
        sys.exit(1)

    label = sys.argv[1]
    data = collections.defaultdict(list)
    for readme_file in sorted(ROOT_PATH.rglob("README.md")):
        metadata = extract_metadata(readme_file)
        if metadata:
            metadata["path"] = readme_file.parent.relative_to(ROOT_PATH)
            for key in metadata.get(label, []):
                data[key].append(metadata)

    for key, projects in sorted(data.items()):
        print(f"{key}: {len(projects)}")
        for project in sorted(projects, key=lambda p: p["title"]):
            print(f"    {project['title']} -- /{project['path']}")
        print()
