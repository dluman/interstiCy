"""Differential parity tests against spaCy.

These tests re-verify token boundaries, text, and whitespace flags every
commit. They are the guardrail for cache-level changes such as the sharded
span cache: the key and partition scheme must not change what spaCy would
produce.
"""

import pytest
import spacy

import intersticy

from .vendor_spacy_tokenizer_tests import (
    SPACY_DEGREE_TESTS,
    SPACY_EMOJI_TESTS,
    SPACY_EMOTICONS_TEXT,
    SPACY_NAUGHTY_STRINGS,
    SPACY_TOKENIZER_TEXTS,
    SPACY_URLS_BASIC,
    SPACY_URLS_FULL,
    SPACY_URLS_SHOULD_MATCH,
    SPACY_URLS_SHOULD_NOT_MATCH,
    SPACY_WHITESPACE_TESTS,
    SUN_TEXT,
)


# Additional edge cases not covered by the vendored spaCy suite.
EXTRA_PARITY_TEXTS = [
    # Curly apostrophes in contractions
    "It’s not what you don’t know that gets you.",
    "I can’t believe you’ve already finished.",
    # Ellipses
    "Wait... what?",
    "So... yeah... no.",
    # En and em dashes
    "The 1990–1999 decade—what a time—was interesting.",
    "Phone: 555–1234.",
    # Decimal numbers and currency
    "The price is $1,234.56 for 3.14159 units.",
    "Temperature: -40.5°F.",
    # Mixed email, URL, and punctuation
    "Contact me at user@example.com or visit https://example.com/path?x=1&y=2.",
    # Smart quotes and nested punctuation
    "She said, ‘Hello, world!’ and then “Goodbye.”",
]

PARITY_TEXTS = (
    SPACY_TOKENIZER_TEXTS
    + SPACY_URLS_BASIC
    + SPACY_URLS_FULL
    + SPACY_URLS_SHOULD_MATCH
    + SPACY_URLS_SHOULD_NOT_MATCH
    + SPACY_WHITESPACE_TESTS
    + SPACY_DEGREE_TESTS
    + [SPACY_EMOTICONS_TEXT]
    + SPACY_EMOJI_TESTS
    + SPACY_NAUGHTY_STRINGS
    + [SUN_TEXT]
    + EXTRA_PARITY_TEXTS
)


@pytest.fixture(scope="module")
def nlp():
    return spacy.blank("en")


@pytest.fixture(scope="module")
def tok():
    return intersticy.Tokenizer.load_from_spacy()


def _assert_span_parity(nlp, tok, text):
    """Assert interstiCy matches spaCy on text, offsets, and whitespace."""
    spacy_doc = nlp(text)
    spans = tok.tokenize_with_spans(text)
    assert len(spans) == len(spacy_doc), (
        f"Token count mismatch for {text!r}: "
        f"spacy={len(spacy_doc)}, intersticy={len(spans)}"
    )
    for (start, end, token_text, has_space), spacy_token in zip(spans, spacy_doc):
        assert token_text == spacy_token.text, (
            f"Text mismatch for {text!r}: "
            f"spacy={spacy_token.text!r}, intersticy={token_text!r}"
        )
        assert start == spacy_token.idx, (
            f"Start offset mismatch for {text!r}: "
            f"spacy={spacy_token.idx}, intersticy={start}"
        )
        assert end == spacy_token.idx + len(spacy_token.text), (
            f"End offset mismatch for {text!r}: "
            f"spacy={spacy_token.idx + len(spacy_token.text)}, intersticy={end}"
        )
        assert has_space == (spacy_token.whitespace_ != ""), (
            f"Whitespace flag mismatch for {text!r}: "
            f"spacy={spacy_token.whitespace_!r}, intersticy={has_space}"
        )


@pytest.mark.parametrize("text", PARITY_TEXTS)
def test_parity_single_text(nlp, tok, text):
    _assert_span_parity(nlp, tok, text)


def test_parity_batch(nlp, tok):
    """Run the full parity corpus through the batch span API."""
    batch = tok.tokenize_with_spans_batch(PARITY_TEXTS)
    assert len(batch) == len(PARITY_TEXTS)
    for text, spans in zip(PARITY_TEXTS, batch):
        spacy_doc = nlp(text)
        assert len(spans) == len(spacy_doc)
        for (start, end, token_text, has_space), spacy_token in zip(spans, spacy_doc):
            assert token_text == spacy_token.text
            assert start == spacy_token.idx
            assert end == spacy_token.idx + len(spacy_token.text)
            assert has_space == (spacy_token.whitespace_ != "")


def test_parity_offsets_batch(nlp, tok):
    """Offsets-only batch API must produce the same offsets as spaCy."""
    batch = tok.tokenize_with_offsets_batch(PARITY_TEXTS)
    assert len(batch) == len(PARITY_TEXTS)
    for text, offsets in zip(PARITY_TEXTS, batch):
        spacy_doc = nlp(text)
        assert len(offsets) == len(spacy_doc)
        for (start, end, has_space), spacy_token in zip(offsets, spacy_doc):
            assert start == spacy_token.idx
            assert end == spacy_token.idx + len(spacy_token.text)
            assert has_space == (spacy_token.whitespace_ != "")


def test_parity_strings_batch(nlp, tok):
    """String-only batch API must produce the same token texts as spaCy."""
    batch = tok.tokenize_batch(PARITY_TEXTS)
    assert len(batch) == len(PARITY_TEXTS)
    for text, tokens in zip(PARITY_TEXTS, batch):
        expected = [t.text for t in nlp(text)]
        assert tokens == expected
