#!/usr/bin/env python3
"""Benchmark interstiCy against spaCy on real-world text and report parity."""
import time
import urllib.request

import spacy

import intersticy

URL = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Pride and Prejudice


def download_text():
    print(f"Downloading {URL} ...")
    with urllib.request.urlopen(URL, timeout=60) as response:
        data = response.read()
    text = data.decode("utf-8", errors="ignore")
    # Strip Project Gutenberg header/footer roughly.
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start != -1 and end != -1:
        text = text[start:end]
    return text


def benchmark(label, func, arg=None, repeat=3):
    # Warm-up.
    if arg is None:
        func()
    else:
        func(arg)
    times = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        if arg is None:
            result = func()
        else:
            result = func(arg)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return min(times), result


def main():
    text = download_text()
    print(f"Text length: {len(text):,} characters")
    print(f"spaCy version: {spacy.__version__}")
    print()

    nlp = spacy.blank("en")
    tok = intersticy.Tokenizer.load_from_spacy()

    def spacy_tokenize(t):
        return [token.text for token in nlp(t)]

    def intersticy_tokenize(t):
        return tok.tokenize(t)

    t_spacy, spacy_tokens = benchmark("spaCy", spacy_tokenize, text)
    t_intersticy, intersticy_tokens = benchmark(
        "interstiCy", intersticy_tokenize, text
    )

    print(f"{'spaCy':20s}  {t_spacy:7.4f}s  {len(text) / t_spacy / 1e6:6.2f} Mchar/s")
    print(f"{'interstiCy':20s}  {t_intersticy:7.4f}s  {len(text) / t_intersticy / 1e6:6.2f} Mchar/s")
    print(f"\nTokenizer-only speedup: {t_spacy / t_intersticy:.2f}x")
    print(
        "Note: this compares tokenizers only (spacy.blank('en')). "
        "End-to-end pipelines (e.g. en_core_web_sm) spend most of their time on "
        "tagging, parsing, and NER, so the overall gain is much smaller."
    )

    # Batch benchmark.
    n_chunks = 128
    chunk_size = 50_000
    chunks = [text[i : i + chunk_size] for i in range(0, n_chunks * chunk_size, chunk_size)]
    print(f"\nBatch benchmark: {len(chunks):,} chunks of ~{chunk_size:,} characters")

    def intersticy_batch():
        return tok.tokenize_with_spans_batch(chunks)

    def intersticy_sequential():
        return [tok.tokenize_with_spans(chunk) for chunk in chunks]

    t_seq, _ = benchmark("interstiCy sequential", intersticy_sequential, None)
    t_batch, _ = benchmark("interstiCy batch (GIL-free)", intersticy_batch, None)
    print(f"  sequential: {t_seq:.4f}s, batch: {t_batch:.4f}s")
    print(f"Batch speedup vs sequential: {t_seq / t_batch:.2f}x")

    # Full parity check.
    print("\nRunning full parity check...")
    assert intersticy_tokens == spacy_tokens, "Token mismatch on full corpus"
    print(f"Parity check passed: {len(spacy_tokens):,} tokens, zero mismatches")

    # Span parity check.
    spans = tok.tokenize_with_spans(text)
    spacy_doc = nlp(text)
    assert len(spans) == len(spacy_doc)
    for (start, end, token_text, has_space), spacy_token in zip(spans, spacy_doc):
        assert token_text == spacy_token.text
        assert start == spacy_token.idx
        assert end == spacy_token.idx + len(spacy_token.text)
        assert has_space == (spacy_token.whitespace_ != "")
    print("Span/whitespace parity check passed.")


if __name__ == "__main__":
    main()
