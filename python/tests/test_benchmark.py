import pytest
import spacy

import intersticy


@pytest.fixture(scope="module")
def large_text():
    # A ~200k-character sample of mixed English text.
    paragraph = (
        "The quick brown fox jumps over the lazy dog. "
        "I don't think e-mail is 100% fun—but it's ok. "
        "Dr. Smith lives at 123 Main St. and pays $10.00 for lunch. "
        "Visit https://example.com for more info. "
        "He said, 'Well, I can't go at 3:30 p.m.' "
        "C++ and C# are languages; (parentheses) and [brackets] are common. "
        "Let's co-operate by 5 o'clock. "
    )
    return paragraph * 1000


@pytest.fixture(scope="module")
def nlp():
    return spacy.blank("en")


@pytest.fixture(scope="module")
def tok():
    return intersticy.Tokenizer.load_from_spacy()


def test_benchmark_spacy(benchmark, nlp, large_text):
    benchmark(nlp, large_text)


def test_benchmark_intersticy(benchmark, tok, large_text):
    benchmark(tok.tokenize, large_text)


def test_benchmark_throughput(tok, large_text):
    # Quick sanity check: intersticy should tokenize the sample.
    tokens = tok.tokenize(large_text)
    assert len(tokens) > 1000
