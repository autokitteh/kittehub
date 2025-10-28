"""Data module for CarbCat."""

import csv
from dataclasses import dataclass
from dataclasses import replace
import gzip
from io import StringIO
from pathlib import Path
import re

import rapidfuzz


@dataclass(frozen=True, kw_only=True)
class Portion:
    """Class representing a portion size."""

    amount: float
    modifier: str
    gram_weight: float


@dataclass(frozen=True, kw_only=True)
class Food:
    """Class representing a row in the data."""

    index: int
    name: str
    carbs: float  # per 100g
    portions: list[Portion]


_foods: list[Food] = []


def _read() -> StringIO:
    """Load raw compressed data."""
    with Path("data.csv.gz").open("rb") as f:
        compressed = f.read()

    return StringIO(gzip.decompress(compressed).decode("utf-8"))


def _load() -> list[Food]:
    """Load food data from CSV file."""
    global _foods

    if not _foods:
        prev: Food | None = None

        r = csv.reader(_read())

        for i, row in enumerate(r):
            curr = Food(
                index=len(_foods),
                name=row[0],
                carbs=float(row[1]),
                portions=[
                    Portion(
                        amount=float(row[2]),
                        modifier=row[3],
                        gram_weight=float(row[4]),
                    )
                ],
            )

            if prev and prev.name == curr.name:
                if prev.carbs != curr.carbs:
                    raise ValueError(
                        f"line #{i + 1}: duplicate food with different carbs: {prev} != {curr}"  # noqa: E501
                    )

                _foods[-1] = replace(
                    prev,
                    index=prev.index,
                    portions=prev.portions + [curr.portions[0]],
                )
            else:
                prev = curr
                _foods.append(curr)

    return _foods


def get_food_by_index(idx: int) -> Food:
    """Get food by its index in the database.

    Args:
        idx: Index of the food.

    Returns:
        Food object.

    Raises:
        IndexError: If the index is out of range.
    """
    foods = _load()
    if idx < 0 or idx >= len(foods):
        raise IndexError(f"Food index {idx} out of range")
    return foods[idx]


def find_foods_by_name(q: str, top_n=100) -> list[tuple[Food, float]]:
    """Search for foods by name and return top N matches.

    Args:
        q: The food name to search for (str)
        top_n: Number of top matches to return (default: 5)

    Returns:
        List of foods and their associated matching scores
    """
    foods = _load()
    food_names = [food.name for food in foods]

    results = [
        (_calculate_food_name_score(q, name), idx)
        for idx, name in enumerate(food_names)
    ]

    # Sort by combined score
    results.sort(key=lambda x: x[0], reverse=True)

    idxs = _smart_cutoff(results)

    # Create a mapping from food index to score
    idx_to_score = {idx: score for score, idx in results}

    return [(foods[i], idx_to_score[i]) for i in idxs[:top_n]]


def _calculate_food_name_score(query: str, food_name: str) -> float:
    """Calculate relevance score for a food name match.

    Args:
        query: The search query
        food_name: The food name to score

    Returns:
        Combined relevance score
    """
    name_lower = food_name.lower()
    q_lower = query.lower()

    # Multiple scoring factors
    wratio_score = rapidfuzz.fuzz.WRatio(query, food_name)
    ratio_score = rapidfuzz.fuzz.ratio(q_lower, name_lower)
    token_sort = rapidfuzz.fuzz.token_sort_ratio(q_lower, name_lower)

    # Split by common delimiters
    words = re.split(r"[\s,\-\(\)]+", name_lower)

    # Check for exact word match and position
    has_exact_word = False
    is_first_word = False
    word_position = len(words)  # Default to end

    for i, word in enumerate(words):
        if word in [q_lower, q_lower + "s", q_lower + "es", q_lower + "ies"]:
            has_exact_word = True
            word_position = i
            if i == 0:
                is_first_word = True
            break

    # Penalize longer names
    length_penalty = 100 / (1 + len(food_name) / 20)

    # Penalize names with many words
    word_count_penalty = 100 / (1 + len(words) / 3)

    # Position bonus - earlier position = higher score
    # First word is MUCH more important (the food IS that thing)
    # vs later words (the food CONTAINS that thing)
    position_bonus = 0
    if has_exact_word:
        if is_first_word:
            position_bonus = 60  # Huge boost for first word (e.g., "Apples, raw")
        elif word_position == 1:
            position_bonus = 5  # Small boost for second word (e.g., "Strudel, apple")
        elif word_position == 2:
            position_bonus = 2  # Tiny boost for third word

    # Calculate combined score
    if has_exact_word:
        combined_score = (
            wratio_score * 0.25
            + ratio_score * 0.25
            + token_sort * 0.15
            + length_penalty * 0.10
            + word_count_penalty * 0.10
            + position_bonus  # Position is very important!
        )
    else:
        combined_score = wratio_score * 0.5 + ratio_score * 0.3 + token_sort * 0.2

    # Check if it's a substring match but NOT a word match
    is_substring_only = q_lower in name_lower and not has_exact_word
    if is_substring_only:
        combined_score *= 0.5  # Heavy penalty for substring-only matches

    return combined_score


def _smart_cutoff(results: list[tuple[float, int]]) -> list[int]:
    """Intelligently determine where to cut off search results based on score drops.

    Args:
        results: List of tuples (score, index) sorted by score descending

    Returns:
        List of indexes to include in final results
    """
    if not results:
        return []

    # Always include at least the top result
    if len(results) == 1:
        return [results[0][1]]

    top_score = results[0][0]

    # Calculate score drops between consecutive results
    score_drops = []
    for i in range(len(results) - 1):
        drop = results[i][0] - results[i + 1][0]
        score_drops.append((i, drop))

    # Find significant drops (> 2 points)
    significant_drops = [(i, drop) for i, drop in score_drops if drop > 2]

    if significant_drops:
        # Sort by drop size to find the largest
        significant_drops.sort(key=lambda x: x[1], reverse=True)
        largest_drop_idx, largest_drop_size = significant_drops[0]

        # Cut at the largest significant drop if it happens reasonably early
        # and is substantial enough
        if largest_drop_idx < 20 and largest_drop_size > 2:
            cutoff = largest_drop_idx + 1
            return [idx for _, idx in results[:cutoff]]

    # If no significant drops, filter by relative score to top result
    # Cut off results that drop below 85% of top score
    cutoff = len(results)
    for i, (score, _) in enumerate(results):
        # If score drops below 85% of top score, cut there
        # But keep at least 5 results
        if i >= 5 and score < (top_score * 0.85):
            cutoff = i
            break

    return [idx for _, idx in results[:cutoff]]
