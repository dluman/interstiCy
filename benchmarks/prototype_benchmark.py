#!/usr/bin/env python3
"""Prototype benchmark for batch APIs."""
import os
import time
import urllib.request

import intersticy

URL = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Pride and Prejudice
N_CHUNKS = 128
CHUNK_SIZE = 50_000
REPEAT = 7


def download_text():
    print(f"Downloading {URL} ...")
    with urllib.request.urlopen(URL, timeout=60) as response:
        text = response.read().decode("utf-8", errors="ignore")
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start != -1 and end != -1:
        text = text[start:end]
    return text


def bench(label, func, n_tokens=None):
    # Warm-up
    result = func()
    times = []
    for _ in range(REPEAT):
        t0 = time.perf_counter()
        result = func()
        t1 = time.perf_counter()
        times.append(t1 - t0)
    best = min(times)
    n_tokens = n_tokens if n_tokens is not None else sum(len(doc) for doc in result)
    throughput = n_tokens / best / 1_000_000
    print(f"{label:42s}  {best:7.4f}s  {n_tokens:>8,} tokens  {throughput:6.2f} Mtok/s")
    return best, result


def main():
    text = download_text()
    print(f"Text length: {len(text):,} characters")
    print(f"Cores: {os.cpu_count()}")
    print()

    chunks = [text[i : i + CHUNK_SIZE] for i in range(0, N_CHUNKS * CHUNK_SIZE, CHUNK_SIZE)]
    print(f"Batch benchmark: {len(chunks):,} chunks of ~{CHUNK_SIZE:,} characters")
    print(f"Repeat: {REPEAT} times (after warm-up)")
    print()

    tok = intersticy.Tokenizer.load_from_spacy()

    # Tokenize once to get a token count.
    spans = tok.tokenize_with_spans_batch(chunks)
    n_tokens = sum(len(doc) for doc in spans)
    print(f"Total tokens: {n_tokens:,}")
    print()

    # --- String-only APIs ---
    t_seq_str, _ = bench(
        "strings sequential",
        lambda: [tok.tokenize(chunk) for chunk in chunks],
        n_tokens,
    )
    t_batch_str, _ = bench(
        "strings batch (GIL-free)",
        lambda: tok.tokenize_batch(chunks),
        n_tokens,
    )
    print(f"  -> batch speedup: {t_seq_str / t_batch_str:.2f}x")
    print()

    # --- Full-span APIs ---
    t_seq_spans, _ = bench(
        "spans sequential (start, end, text, space)",
        lambda: [tok.tokenize_with_spans(chunk) for chunk in chunks],
        n_tokens,
    )
    t_batch_spans, _ = bench(
        "spans batch (GIL-free, includes text)",
        lambda: tok.tokenize_with_spans_batch(chunks),
        n_tokens,
    )
    print(f"  -> batch speedup: {t_seq_spans / t_batch_spans:.2f}x")
    print()

    # --- Offsets-only APIs ---
    t_seq_offsets, _ = bench(
        "offsets sequential (start, end, space)",
        lambda: [tok.tokenize_with_offsets(chunk) for chunk in chunks],
        n_tokens,
    )
    t_batch_offsets, _ = bench(
        "offsets batch (GIL-free, no text)",
        lambda: tok.tokenize_with_offsets_batch(chunks),
        n_tokens,
    )
    print(f"  -> batch speedup: {t_seq_offsets / t_batch_offsets:.2f}x")
    print()

    # Summary
    print("Summary:")
    print(f"  8-core ideal scaling: {os.cpu_count():.0f}x")
    print(f"  strings batch:        {t_seq_str / t_batch_str:.2f}x")
    print(f"  spans batch:          {t_seq_spans / t_batch_spans:.2f}x")
    print(f"  offsets batch:        {t_seq_offsets / t_batch_offsets:.2f}x")
    print()
    print("Batch scaling is limited by the total Rust tokenization work and")
    print("thread-scheduling overhead when each chunk is small. A sharded span")
    print("cache improved the speedup over the original single-mutex cache.")


if __name__ == "__main__":
    main()
