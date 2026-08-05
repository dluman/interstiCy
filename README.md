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

Benchmarks are measured against `spacy.blank("en")` (the tokenizer only) on the
same machine and text. End-to-end pipelines such as `en_core_web_sm` spend most
of their time on tagging, parsing, and NER, so the overall speedup there is much
smaller than the tokenizer-only figures below.

| Workload | spaCy | interstiCy | Result |
|---|---|---|---|
| Repetitive English paragraph (cached, ~200 k chars) | ~218 ms | ~17 ms | **~13x** (cache-heavy) |
| Real-world prose (Pride and Prejudice, 728 k chars) | ~599 ms | ~256 ms | **~2.3x** tokenizer-only |
| 128 chunks of ~50 k chars, sequential vs batch | — | — | **1.8x** batch speedup |

Run the standalone benchmark yourself:

```bash
python benchmarks/benchmark.py
```

The script downloads the public-domain Project Gutenberg text of *Pride and
Prejudice* and reports both single-text and batch throughput.

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
