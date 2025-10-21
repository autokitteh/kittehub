"""Tests for ai.py, this is interactive so not run by default."""

import ai
import pytest


@pytest.mark.skip(reason="interactive test, disable skip to play around")
def test_interact():
    # Requires ANTHROPIC_API_KEY defined in env.

    def get_next() -> str:
        return input("> ")

    print(ai.interact("", get_next, print))
