import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1])) # Adjust path to allow imports from scripts directory

import pytest
from scripts.load import extract_quarter_key


def test_sanity():
    assert 1 + 1 == 2
    
# Test extract_quarter_key with valid input
@pytest.mark.parametrize("input_str, expected", [
    ("Q1 2022", (2022, 1)),
    ("Q4 2020", (2020, 4)),
    ("Q2 2019", (2019, 2)),
])
def test_extract_quarter_key_valid(input_str, expected):
    assert extract_quarter_key(input_str) == expected

# Test extract_quarter_key with invalid input
@pytest.mark.parametrize("input_str", [
    "2022 Q1", "Quarter 2 2020", "SomethingElse", ""
])
def test_extract_quarter_key_invalid(input_str):
    assert extract_quarter_key(input_str) == (0, 0)
