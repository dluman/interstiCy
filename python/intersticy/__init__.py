"""interstiCy: a fast Rust implementation of spaCy tokenization."""

from ._intersticy import Tokenizer
from .tokenizer import create_tokenizer, IntersticyTokenizer

__all__ = [
    "Tokenizer",
    "IntersticyTokenizer",
    "create_tokenizer",
]

__version__ = "0.1.0"
