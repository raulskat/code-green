import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from HackX.rule_model import (
    detect_exact_match,
    detect_variable_renaming,
    detect_structural_similarity,
)


def test_detect_exact_match_ignores_comments_and_whitespace():
    original = "def add(a, b):\n    return a + b"
    test = "def add(a, b):    # comment\n    return a + b  "
    assert detect_exact_match(original, test)


def test_detect_exact_match_false_on_different_code():
    original = "def add(a, b): return a + b"
    test = "def sub(a, b): return a - b"
    assert not detect_exact_match(original, test)


def test_detect_variable_renaming_success():
    original = "def add(a, b): return a + b"
    test = "def add(x, y): return x + y"
    assert detect_variable_renaming(original, test)


def test_detect_variable_renaming_inconsistent_mapping():
    original = "def add(a, b): return a + b"
    test = "def add(x, y): return x + b"
    assert not detect_variable_renaming(original, test)


def test_detect_structural_similarity_loops():
    original = "for i in range(10):\n    print(i)"
    test = "i = 0\nwhile i < 10:\n    print(i)\n    i += 1"
    assert detect_structural_similarity(original, test)


def test_detect_structural_similarity_different_structures():
    original = "for i in range(10):\n    print(i)"
    test = "if a > b:\n    print(a)"
    assert not detect_structural_similarity(original, test)
