# interstiCy

A fast Rust implementation of spaCy tokenization with Python bindings.

> [!NOTE]
> Interested in a fuller implementation of spaCy bindings in Rust? Checkout
> [rusTy](https://www.github.com/dluman/rusTy).

## Overview

`interstiCy` is a Rust reimplementation of spaCy's English tokenizer, exposed to
Python via PyO3 and maturin. It aims to be a drop-in tokenizer replacement for
`spacy.blank("en")` and produces matching token boundaries, whitespace flags, and
character-level spans.

**Current scope:** English only. Multi-language support is planned, but the
rules and special-case loader are English-specific until loaders for other
languages are added.

## API

**Default entry points:**

- For spaCy integration: `intersticy.create_tokenizer(nlp)`
- For direct batch use: `Tokenizer.load_from_spacy().tokenize_with_spans_batch(texts)`

The detailed API is the primary interface:

```python
from intersticy import Tokenizer

tok = Tokenizer.load_from_spacy()

# Single text, returns (start_char, end_char, text, has_space_after)
for start, end, text, space in tok.tokenize_with_spans("Hello, world!"):
    print(repr(text), start, end, space)
# ('Hello', 0, 5, False)
# (',', 5, 6, True)
# ('world', 7, 12, False)
# ('!', 12, 13, False)

# Batch, releases the GIL and tokenizes across cores
results = tok.tokenize_with_spans_batch([text1, text2, ...])

# String-only batch (no offsets, less overhead)
words = tok.tokenize_batch([text1, text2, ...])

# Offsets-only batch (no per-token PyString allocation)
spans = tok.tokenize_with_offsets_batch([text1, text2, ...])
# Each tuple is (start_char, end_char, has_space_after); recover text with text[start:end]
```

A string-only convenience method is also available:

```python
print(tok.tokenize("Hello, world!"))
# ['Hello', ',', 'world', '!']
```

For spaCy integration, wrap the tokenizer as a replacement:

```python
import spacy
import intersticy

nlp = spacy.load("en_core_web_sm")
nlp.tokenizer = intersticy.create_tokenizer(nlp)

doc = nlp("Hello, world!")
print([t.text for t in doc])
# ['Hello', ',', 'world', '!']
```

## Benchmarks

All timings are for tokenization only, measured against `spacy.blank("en")` on the
same machine and text.

| Workload | spaCy | interstiCy | Speedup |
|---|---|---|---|
| Repetitive English paragraph (~200 k chars, cache-heavy) | ~218 ms | ~17 ms | **~13x** |
| Real-world prose (Pride and Prejudice, 728 k chars) | ~700 ms | ~60 ms | **~11.8x** |
| 128 chunks of ~50 k chars, batch vs sequential | — | — | **~2.2x on 8 cores** |

Batch APIs release the GIL and run across all cores. Larger chunks generally
scale better; end-to-end pipelines spend most of their time on tagging, parsing,
and NER, so the overall speedup there is smaller than the tokenizer-only figures
above.

Run the standalone benchmarks yourself:

```bash
python benchmarks/benchmark.py
python benchmarks/prototype_benchmark.py
```

The first script downloads the public-domain Project Gutenberg text of *Pride and
Prejudice* and reports both single-text and batch throughput. The second
script compares the different batch APIs and a Rust-only count to show where the
batch scaling ceiling comes from.

## Parity

`interstiCy` is tested against spaCy for byte-level token boundaries, text, and
whitespace flags.

Latest reported run (spaCy 3.8.14):

- **Corpus:** Project Gutenberg, *Pride and Prejudice*
- **Text length:** 728,798 characters
- **Token count:** 164,234 tokens
- **Mismatches:** 0
- **Span/whitespace parity:** passed

## Installation

```bash
pip install intersticy
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT
