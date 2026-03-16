import pytest
from wrapper.content_processing.info_extractor import InfoExtractor

@pytest.fixture
def extractor():
    return InfoExtractor()

def test_extract_info_success(extractor):
    text = "The quick brown fox. Jumps over the lazy dog. Aethera is awesome."
    keywords = ["fox", "Aethera"]
    expected = ["The quick brown fox", "Aethera is awesome"]
    assert extractor.extract_info(text, keywords) == expected

def test_extract_info_empty_text(extractor):
    text = ""
    keywords = ["fox"]
    assert extractor.extract_info(text, keywords) == []

def test_extract_info_empty_keywords(extractor):
    text = "The quick brown fox."
    keywords = []
    assert extractor.extract_info(text, keywords) == []

def test_extract_info_no_match(extractor):
    text = "The quick brown fox."
    keywords = ["cat"]
    assert extractor.extract_info(text, keywords) == []

def test_extract_info_case_insensitive(extractor):
    text = "The Quick Brown Fox."
    keywords = ["fox"]
    assert extractor.extract_info(text, keywords) == ["The Quick Brown Fox"]

def test_extract_info_multiple_keywords_in_one_sentence(extractor):
    text = "The quick brown fox and the cat."
    keywords = ["fox", "cat"]
    assert extractor.extract_info(text, keywords) == ["The quick brown fox and the cat"]
