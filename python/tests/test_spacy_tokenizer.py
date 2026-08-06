"""Tests adapted from the spaCy tokenizer test suite.

These tests mirror the inputs spaCy uses to validate its own tokenizer and
assert that interstiCy produces the same token boundaries as
``spacy.blank("en").tokenizer`` for those inputs.

The vendored test data is in ``vendor_spacy_tokenizer_tests.py`` and is
derived from the spaCy test suite (MIT License).
"""

from pathlib import Path

import pytest
import spacy

import intersticy

from .vendor_spacy_tokenizer_tests import (
    SPACY_DEGREE_TESTS,
    SPACY_EMOJI_TESTS,
    SPACY_EMOTICONS_TEXT,
    SPACY_NAUGHTY_STRINGS,
    SPACY_TOKENIZER_TEXTS,
    SPACY_URL_PREFIXES,
    SPACY_URL_SUFFIXES,
    SPACY_URLS_BASIC,
    SPACY_URLS_FULL,
    SPACY_URLS_SHOULD_MATCH,
    SPACY_URLS_SHOULD_NOT_MATCH,
    SPACY_WHITESPACE_TESTS,
    SUN_TEXT,
)


@pytest.fixture(scope="module")
def spacy_tokenizer():
    """A fresh spaCy English tokenizer."""
    return spacy.blank("en").tokenizer


@pytest.fixture(scope="module")
def inter_tokenizer():
    """An interstiCy tokenizer wrapped as a spaCy-compatible callable."""
    nlp = spacy.blank("en")
    return intersticy.create_tokenizer(nlp)


def _token_texts(doc):
    return [token.text for token in doc]


def _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text):
    """Assert interstiCy tokenizes ``text`` the same as spaCy."""
    expected = _token_texts(spacy_tokenizer(text))
    got = _token_texts(inter_tokenizer(text))
    assert got == expected, f"Tokenization mismatch for: {text!r}\nexpected: {expected}\ngot:      {got}"


@pytest.mark.parametrize("text", SPACY_TOKENIZER_TEXTS)
def test_spacy_tokenizer_texts(spacy_tokenizer, inter_tokenizer, text):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text)


@pytest.mark.parametrize("text", SPACY_URLS_BASIC)
def test_spacy_urls_basic(spacy_tokenizer, inter_tokenizer, text):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text)


@pytest.mark.parametrize("text", SPACY_URLS_FULL)
def test_spacy_urls_full(spacy_tokenizer, inter_tokenizer, text):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text)


@pytest.mark.parametrize("text", SPACY_URLS_SHOULD_MATCH)
def test_spacy_urls_should_match(spacy_tokenizer, inter_tokenizer, text):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text)


@pytest.mark.parametrize("text", SPACY_URLS_SHOULD_NOT_MATCH)
def test_spacy_urls_should_not_match(spacy_tokenizer, inter_tokenizer, text):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text)


@pytest.mark.parametrize("prefix", SPACY_URL_PREFIXES)
@pytest.mark.parametrize("suffix", SPACY_URL_SUFFIXES)
@pytest.mark.parametrize("url", SPACY_URLS_FULL)
def test_spacy_url_prefix_suffix(spacy_tokenizer, inter_tokenizer, prefix, suffix, url):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, prefix + url + suffix)


@pytest.mark.parametrize("prefix", SPACY_URL_PREFIXES)
@pytest.mark.parametrize("prefix2", SPACY_URL_PREFIXES)
@pytest.mark.parametrize("url", SPACY_URLS_FULL)
def test_spacy_two_url_prefixes(spacy_tokenizer, inter_tokenizer, prefix, prefix2, url):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, prefix + prefix2 + url)


@pytest.mark.parametrize("suffix", SPACY_URL_SUFFIXES)
@pytest.mark.parametrize("suffix2", SPACY_URL_SUFFIXES)
@pytest.mark.parametrize("url", SPACY_URLS_FULL)
def test_spacy_two_url_suffixes(spacy_tokenizer, inter_tokenizer, suffix, suffix2, url):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, url + suffix + suffix2)


@pytest.mark.parametrize("text", SPACY_WHITESPACE_TESTS)
def test_spacy_whitespace(spacy_tokenizer, inter_tokenizer, text):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text)


@pytest.mark.parametrize("text", SPACY_DEGREE_TESTS)
def test_spacy_degree(spacy_tokenizer, inter_tokenizer, text):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text)


def test_spacy_emoticons(spacy_tokenizer, inter_tokenizer):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, SPACY_EMOTICONS_TEXT)


@pytest.mark.parametrize("text", SPACY_EMOJI_TESTS)
def test_spacy_emoji(spacy_tokenizer, inter_tokenizer, text):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text)


@pytest.mark.parametrize("text", SPACY_NAUGHTY_STRINGS)
def test_spacy_naughty_strings(spacy_tokenizer, inter_tokenizer, text):
    # These are adversarial / edge-case strings. The primary goal is that
    # interstiCy does not crash and preserves the original text. We also assert
    # tokenization matches spaCy where possible; known mismatches are handled via
    # pytest.xfail in the data file.
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text)


def test_spacy_sun_text(spacy_tokenizer, inter_tokenizer):
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, SUN_TEXT)


def test_spacy_sun_text_from_file(spacy_tokenizer, inter_tokenizer):
    """If the vendored sun.txt corpus is present, tokenize it exactly like spaCy."""
    path = Path(__file__).parent / "data" / "sun.txt"
    if not path.exists():
        pytest.skip("vendored sun.txt corpus not present")
    text = path.read_text(encoding="utf-8")
    _assert_tokenization_matches(spacy_tokenizer, inter_tokenizer, text)
