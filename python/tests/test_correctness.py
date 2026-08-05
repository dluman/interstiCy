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
