"""Python-side spaCy integration for interstiCy."""

from typing import Any

from spacy.tokens import Doc

from ._intersticy import Tokenizer


class IntersticyTokenizer:
    """A spaCy-compatible tokenizer backed by the Rust interstiCy engine.

    Instances of this class can be assigned directly to ``nlp.tokenizer``:

        >>> import spacy
        >>> import intersticy
        >>> nlp = spacy.load("en_core_web_sm")
        >>> nlp.tokenizer = intersticy.create_tokenizer(nlp)
    """

    def __init__(self, vocab, tokenizer: Tokenizer):
        self.vocab = vocab
        self._tokenizer = tokenizer

    def __call__(self, text: str) -> Doc:
        words_spaces = self._tokenizer.tokenize_with_spaces(text)
        words = [w for w, _ in words_spaces]
        spaces = [s for _, s in words_spaces]
        return Doc(self.vocab, words=words, spaces=spaces)

    def tokenize(self, text: str) -> list[str]:
        """Return token strings (convenience method)."""
        return self._tokenizer.tokenize(text)

    def tokenize_with_spans(self, text: str) -> list[tuple[int, int, str, bool]]:
        """Return `(start_char, end_char, text, has_space_after)` tuples."""
        return self._tokenizer.tokenize_with_spans(text)

    def tokenize_with_offsets(self, text: str) -> list[tuple[int, int, bool]]:
        """Return `(start_char, end_char, has_space_after)` tuples."""
        return self._tokenizer.tokenize_with_offsets(text)

    def tokenize_batch(self, texts: list[str]) -> list[list[str]]:
        """Return token strings for a list of texts, releasing the GIL."""
        return self._tokenizer.tokenize_batch(texts)

    def tokenize_with_spans_batch(
        self, texts: list[str]
    ) -> list[list[tuple[int, int, str, bool]]]:
        """Return spans for a list of texts, releasing the GIL and using all cores."""
        return self._tokenizer.tokenize_with_spans_batch(texts)

    def tokenize_with_offsets_batch(
        self, texts: list[str]
    ) -> list[list[tuple[int, int, bool]]]:
        """Return `(start_char, end_char, has_space_after)` tuples for a list of texts.

        The token text is omitted; use `text[start:end]` to recover it.  This
        avoids the per-token PyString allocation, but batch scaling is still
        limited by the total Rust tokenization work and thread-scheduling
        overhead when chunks are small.
        """
        return self._tokenizer.tokenize_with_offsets_batch(texts)


def create_tokenizer(nlp: Any) -> IntersticyTokenizer:
    """Create an interstiCy tokenizer from a spaCy ``Language`` object.

    The returned object can replace ``nlp.tokenizer``.
    """
    tokenizer = Tokenizer.load_from_spacy()
    return IntersticyTokenizer(nlp.vocab, tokenizer)
