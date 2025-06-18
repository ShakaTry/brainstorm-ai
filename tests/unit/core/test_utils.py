import pytest
from brainstorm_ai.core.utils import dedupe, extract_numbered_ideas

def test_dedupe():
    """
    Tests the dedupe function to ensure it removes duplicates,
    strips whitespace, and removes empty entries.
    """
    ideas = ["  idea 1  ", "idea 2", "  idea 1  ", "idea 3", "", "  "]
    expected = ["idea 1", "idea 2", "idea 3"]
    assert dedupe(ideas) == expected

def test_dedupe_empty_list():
    """
    Tests the dedupe function with an empty list.
    """
    assert dedupe([]) == []

def test_extract_numbered_ideas():
    """
    Tests the extract_numbered_ideas function to ensure it extracts
    only lines starting with a digit.
    """
    text = """
1. First idea.
2. Second idea.
- A bullet point.
3. Third idea.
Not a numbered idea.
    """
    expected = ["1. First idea.", "2. Second idea.", "3. Third idea."]
    assert extract_numbered_ideas(text) == expected

def test_extract_numbered_ideas_empty_string():
    """
    Tests the extract_numbered_ideas function with an empty string.
    """
    assert extract_numbered_ideas("") == []

def test_extract_numbered_ideas_no_matches():
    """
    Tests the extract_numbered_ideas function with text containing no numbered lines.
    """
    text = "No numbered ideas here.\n- Just bullet points."
    assert extract_numbered_ideas(text) == []

if __name__ == '__main__':
    pytest.main() 