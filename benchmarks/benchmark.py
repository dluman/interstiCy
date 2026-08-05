#!/usr/bin/env python3
"""Benchmark interstiCy against spaCy on real-world text."""
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


def benchmark(label, func, text, repeat=3):
    # Warm-up.
    func(text)
    times = []
    for _ in range(repeat):
        t0 = time.perf_counter()
        result = func(text)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    mean = sum(times) / len(times)
    chars = len(text)
    if isinstance(result, list):
        tokens = len(result)
    else:
        tokens = len(result)
    print(f"{label:20s}  {mean:7.4f}s  {chars / mean / 1e6:6.2f} Mchar/s  {tokens / mean / 1e3:6.2f} ktokens/s")
    return mean


def main():
    text = download_text()
    print(f"Text length: {len(text):,} characters")

    nlp = spacy.blank("en")
    tok = intersticy.Tokenizer.load_from_spacy()

    def spacy_tokenize(t):
        return [token.text for token in nlp(t)]

    def intersticy_tokenize(t):
        return tok.tokenize(t)

    t_spacy = benchmark("spaCy", spacy_tokenize, text)
    t_intersticy = benchmark("interstiCy", intersticy_tokenize, text)

    speedup = t_spacy / t_intersticy
    print(f"\nSpeedup: {speedup:.2f}x")

    # Correctness check on a sample.
    sample = text[:5000]
    assert tok.tokenize(sample) == [t.text for t in nlp(sample)]
    print("Correctness check passed on first 5,000 characters.")


if __name__ == "__main__":
    main()
