"""Tests for data module food database loading and search functionality."""

import data


def test_load():
    foods = data._load()
    assert foods
    assert all(foods[i].index == i for i in range(len(foods)))


def test_find_foods_by_name():
    results = data.find_foods_by_name("apple")
    print("\n".join(str(x) for x in results))
    assert results
    assert all(f.name.startswith("Apple") for f, _ in results)
