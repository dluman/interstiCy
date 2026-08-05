#!/usr/bin/env python3
"""Dump spaCy English tokenizer rules and special cases for Rust implementation."""
import json
import re

from spacy.lang.en import English
from spacy.symbols import NORM, ORTH


def _get_pattern(regex_func):
    """Extract the regex pattern string from a compiled regex function."""
    if regex_func is None:
        return None
    # spaCy passes the compiled regex object's method as the callable.
    regex_obj = getattr(regex_func, "__self__", None)
    if regex_obj is None:
        return None
    return getattr(regex_obj, "pattern", None)


def _extract_spec(spec):
    """Extract ORTH and NORM strings from a spaCy special-case spec dict."""
    result = {}
    if ORTH in spec:
        result["ORTH"] = spec[ORTH]
    if NORM in spec:
        result["NORM"] = spec[NORM]
    return result


def main():
    nlp = English()
    tok = nlp.tokenizer

    rules = {}
    for orth, attrs in tok.rules.items():
        rules[orth] = [_extract_spec(spec) for spec in attrs]

    data = {
        "prefix": _get_pattern(tok.prefix_search),
        "suffix": _get_pattern(tok.suffix_search),
        "infix": _get_pattern(tok.infix_finditer),
        "token_match": _get_pattern(tok.token_match),
        "url_match": _get_pattern(tok.url_match),
        "faster_heuristics": tok.faster_heuristics,
        "rules": rules,
    }

    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
