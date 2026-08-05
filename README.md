# interstiCy

A fast Rust implementation of spaCy tokenization with Python bindings.

## Overview

`interstiCy` speeds up spaCy's tokenizer by implementing the tokenization
rules in Rust and exposing them to Python via PyO3/maturin. It produces
token boundaries that match spaCy for supported languages.

## Benchmarks

Benchmarks are run with `pytest-benchmark` on the same CPU and text. Results
vary with hardware and text characteristics, but typical numbers are:

| Text type | spaCy | interstiCy | Speedup |
|---|---|---|---|
| Repetitive English paragraph (cached, ~200k chars) | ~218 ms | ~17 ms | **~13x** |
| Real-world prose (Pride and Prejudice, 728k chars) | ~616 ms | ~272 ms | **~2.3x** |

Run the standalone benchmark script yourself:

```bash
python benchmarks/benchmark.py
```

This downloads a public-domain text from Project Gutenberg and compares
`intersticy.Tokenizer.tokenize()` against `spacy.blank("en")`.

## Installation

```bash
pip install intersticy
```

## Usage

```python
import spacy
import intersticy

nlp = spacy.load("en_core_web_sm")
nlp.tokenizer = intersticy.create_tokenizer(nlp)

doc = nlp("Hello, world!")
print([t.text for t in doc])
# ['Hello', ',', 'world', '!']
```

You can also use the standalone tokenizer:

```python
from intersticy import Tokenizer

tok = Tokenizer.load_from_spacy()
print(tok.tokenize("Hello, world!"))
# ['Hello', ',', 'world', '!']
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
