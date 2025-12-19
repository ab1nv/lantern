
from lantern.utils import (
    extract_question_slug,
    format_question_id,
    get_language_extension,
)


def test_extract_question_slug():
    url1 = "https://leetcode.com/problems/two-sum/"
    assert extract_question_slug(url1) == "two-sum"
    
    url2 = "https://leetcode.com/problems/two-sum/description/"
    assert extract_question_slug(url2) == "two-sum"
    
    url3 = "https://leetcode.com/problems/valid-parentheses"
    assert extract_question_slug(url3) == "valid-parentheses"
    
    url4 = "https://invalid-url.com"
    assert extract_question_slug(url4) is None


def test_format_question_id():
    assert format_question_id("1") == "0001"
    assert format_question_id("245") == "0245"
    assert format_question_id("1834") == "1834"
    assert format_question_id("42") == "0042"


def test_get_language_extension():
    assert get_language_extension("python") == "py"
    assert get_language_extension("Python") == "py"
    assert get_language_extension("go") == "go"
    assert get_language_extension("java") == "java"
    assert get_language_extension("cpp") == "cpp"
    assert get_language_extension("unknown") == "py"

