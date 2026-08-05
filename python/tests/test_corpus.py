"""Corpus-level parity check against spaCy.

Downloads Pride and Prejudice from Project Gutenberg and asserts that
interstiCy produces exactly the same token sequence as spaCy's English
blank tokenizer.
"""

import urllib.request

import pytest
import spacy

import intersticy

URL = "https://www.gutenberg.org/files/1342/1342-0.txt"


@pytest.fixture(scope="module")
def corpus_text():
    try:
        with urllib.request.urlopen(URL, timeout=60) as response:
            data = response.read()
    except Exception as exc:
        pytest.skip(f"Could not download corpus: {exc}")

    text = data.decode("utf-8", errors="ignore")
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start != -1 and end != -1:
        text = text[start:end]
    return text


@pytest.fixture(scope="module")
def nlp():
    return spacy.blank("en")


@pytest.fixture(scope="module")
def tok():
    return intersticy.Tokenizer.load_from_spacy()


def test_corpus_token_parity(corpus_text, nlp, tok):
    rust_tokens = tok.tokenize(corpus_text)
    spacy_tokens = [t.text for t in nlp(corpus_text)]
    assert rust_tokens == spacy_tokens, (
        f"Token mismatch on {len(corpus_text):,} characters: "
        f"{len(rust_tokens)} interstiCy tokens vs {len(spacy_tokens)} spaCy tokens"
    )


def test_corpus_span_parity(corpus_text, nlp, tok):
    spans = tok.tokenize_with_spans(corpus_text)
    spacy_doc = nlp(corpus_text)
    assert len(spans) == len(spacy_doc)
    for (start, end, text, has_space), spacy_token in zip(spans, spacy_doc):
        assert text == spacy_token.text
        assert start == spacy_token.idx
        assert end == spacy_token.idx + len(spacy_token.text)
        assert has_space == (spacy_token.whitespace_ != "")
