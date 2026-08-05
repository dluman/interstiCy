import spacy
import pytest

import intersticy


@pytest.fixture
def nlp():
    return spacy.blank("en")


@pytest.fixture
def tok():
    return intersticy.Tokenizer.load_from_spacy()


@pytest.mark.parametrize(
    "text",
    [
        "Hello, world!",
        "I don't think e-mail is 100% fun—but it's ok.",
        "Visit https://example.com for $10.",
        "She said, 'Well, I can't.'",
        "The U.S. is a country. Dr. Smith lives at 123 Main St.",
        "Emails: user@example.com and admin@site.org.",
        "Let's meet at 3:30 p.m. or 4 p.m.?",
        "He'll've finished by 5 o'clock.",
        "One-two-three—go!",
        "(parenthetical) [bracketed] {braced}",
        "‘Single’ and “double” quotes",
        "C++ and C# are languages.",
        "It's 100°F outside.",
        "a.b.c.d",
        "co-operate vs cooperate",
        "Hello  world",
        "Hello\tworld",
        "Hello\n\nworld",
        "  Hello  world  ",
        " ",
        "\n",
    ],
)
def test_tokenize_matches_spacy(nlp, tok, text):
    spacy_tokens = [t.text for t in nlp(text)]
    rust_tokens = tok.tokenize(text)
    assert rust_tokens == spacy_tokens, f"Mismatch for: {text!r}"


def test_tokenize_with_spans_matches_doc(nlp, tok):
    text = "Hello, world! I do n't know."
    spacy_doc = nlp(text)
    spans = tok.tokenize_with_spans(text)
    assert len(spans) == len(spacy_doc)
    for (start, end, token_text, has_space), spacy_token in zip(spans, spacy_doc):
        assert token_text == spacy_token.text
        assert start == spacy_token.idx
        assert end == spacy_token.idx + len(spacy_token.text)
        assert has_space == (spacy_token.whitespace_ != "")


def test_tokenize_with_spans_batch_matches_spacy(nlp, tok):
    texts = [
        "Hello, world!",
        "I don't think e-mail is 100% fun—but it's ok.",
        "Visit https://example.com for $10.",
    ]
    batch = tok.tokenize_with_spans_batch(texts)
    assert len(batch) == len(texts)
    for text, spans in zip(texts, batch):
        spacy_doc = nlp(text)
        assert len(spans) == len(spacy_doc)
        for (start, end, token_text, has_space), spacy_token in zip(spans, spacy_doc):
            assert token_text == spacy_token.text
            assert start == spacy_token.idx
            assert end == spacy_token.idx + len(spacy_token.text)
            assert has_space == (spacy_token.whitespace_ != "")


def test_tokenize_with_spaces_matches_doc(nlp, tok):
    text = "Hello, world! I do n't know."
    wrapper = intersticy.IntersticyTokenizer(nlp.vocab, tok)
    doc = wrapper(text)
    spacy_doc = nlp(text)
    assert [t.text for t in doc] == [t.text for t in spacy_doc]
    assert [t.whitespace_ for t in doc] == [t.whitespace_ for t in spacy_doc]


def test_create_tokenizer_replacement(nlp):
    nlp.tokenizer = intersticy.create_tokenizer(nlp)
    doc = nlp("Hello, world!")
    assert [t.text for t in doc] == ["Hello", ",", "world", "!"]


def test_intersticy_tokenizer_wraps_batch(nlp, tok):
    wrapper = intersticy.IntersticyTokenizer(nlp.vocab, tok)
    texts = ["Hello, world!", "Goodbye, world!"]
    batch = wrapper.tokenize_with_spans_batch(texts)
    assert len(batch) == 2
    assert batch[0][0] == (0, 5, "Hello", False)
    assert batch[0][1] == (5, 6, ",", True)
    assert batch[0][2] == (7, 12, "world", False)
    assert batch[0][3] == (12, 13, "!", False)
