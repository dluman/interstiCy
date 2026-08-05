use crate::rules::{SpaCyRuleSpec, SpaCyRules};
use crate::special_cases::TokenSequenceTrie;
use crate::token::Token;
use fancy_regex::Regex;
use std::collections::HashMap;
use std::sync::Mutex;

const SPAN_CACHE_LIMIT: usize = 10_000;

/// A spaCy-compatible tokenizer implemented in Rust.
pub struct Tokenizer {
    prefix_re: Regex,
    suffix_re: Regex,
    infix_re: Regex,
    token_match: Option<Regex>,
    url_match: Option<Regex>,
    single_special_cases: HashMap<String, Vec<SpaCyRuleSpec>>,
    multi_special_cases: TokenSequenceTrie,
    /// Cache for `tokenize_span` results. The key is (span text, use_special_cases).
    span_cache: Mutex<HashMap<(String, bool), Vec<Token>>>,
}

impl std::fmt::Debug for Tokenizer {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Tokenizer")
            .field("special_cases", &self.single_special_cases.len())
            .finish_non_exhaustive()
    }
}

impl Tokenizer {
    /// Construct a tokenizer from a spaCy-style rule set.
    pub fn from_spacy_rules(rules: &SpaCyRules) -> Result<Self, fancy_regex::Error> {
        let empty_re = Regex::new("a^")?;

        let raw = Self {
            prefix_re: rules
                .prefix
                .as_deref()
                .map(Regex::new)
                .transpose()?
                .unwrap_or_else(|| empty_re.clone()),
            suffix_re: rules
                .suffix
                .as_deref()
                .map(Regex::new)
                .transpose()?
                .unwrap_or_else(|| empty_re.clone()),
            infix_re: rules
                .infix
                .as_deref()
                .map(Regex::new)
                .transpose()?
                .unwrap_or_else(|| empty_re.clone()),
            token_match: rules
                .token_match
                .as_deref()
                .map(Regex::new)
                .transpose()?,
            url_match: rules
                .url_match
                .as_deref()
                .map(Regex::new)
                .transpose()?,
            single_special_cases: HashMap::new(),
            multi_special_cases: TokenSequenceTrie::new(),
            span_cache: Mutex::new(HashMap::new()),
        };

        // Compute single- vs multi-token special cases.
        let mut single = HashMap::new();
        let mut multi = TokenSequenceTrie::new();
        for (orth, specs) in &rules.rules {
            let key_tokens = raw.tokenize_affixes(orth, false);
            let key: Vec<String> = key_tokens.into_iter().map(|t| t.text).collect();
            if key.len() <= 1 {
                single.insert(orth.clone(), specs.clone());
            } else {
                multi.insert(key, specs.clone());
            }
        }

        Ok(Self {
            prefix_re: raw.prefix_re,
            suffix_re: raw.suffix_re,
            infix_re: raw.infix_re,
            token_match: raw.token_match,
            url_match: raw.url_match,
            single_special_cases: single,
            multi_special_cases: multi,
            span_cache: raw.span_cache,
        })
    }

    /// Tokenize a string and return the resulting token sequence.
    pub fn tokenize(&self, text: &str) -> Vec<Token> {
        let mut initial = self.tokenize_affixes(text, true);
        initial = self.apply_multi_special_cases(initial);
        initial
    }

    /// Return only the token texts.
    pub fn tokenize_texts(&self, text: &str) -> Vec<String> {
        self.tokenize(text).into_iter().map(|t| t.text).collect()
    }

    /// Tokenize the full text using affix rules only.
    ///
    /// This mirrors spaCy's `_tokenize_affixes` and is the first pass before
    /// multi-token special cases are applied.
    fn tokenize_affixes(&self, text: &str, use_special_cases: bool) -> Vec<Token> {
        let mut tokens = Vec::new();
        let mut char_indices = text.char_indices().peekable();

        while let Some((start, ch)) = char_indices.next() {
            let is_whitespace = ch.is_whitespace();
            // Find the end of the current span.
            while let Some((_, next_ch)) = char_indices.peek() {
                if next_ch.is_whitespace() != is_whitespace {
                    break;
                }
                char_indices.next();
            }
            let end = char_indices
                .peek()
                .map(|(offset, _)| *offset)
                .unwrap_or(text.len());
            let span_text = &text[start..end];

            if is_whitespace {
                self.process_whitespace_span(span_text, start, end, &mut tokens);
            } else {
                self.process_non_whitespace_span(
                    span_text,
                    start,
                    end,
                    use_special_cases,
                    &mut tokens,
                );
            }
        }

        tokens
    }

    fn process_non_whitespace_span(
        &self,
        span_text: &str,
        start: usize,
        _end: usize,
        use_special_cases: bool,
        tokens: &mut Vec<Token>,
    ) {
        let span_tokens = self.tokenize_span_cached(span_text, use_special_cases);
        for token in span_tokens {
            tokens.push(Token::new(
                token.start + start,
                token.end + start,
                token.text,
                false,
            ));
        }
    }

    fn process_whitespace_span(
        &self,
        span_text: &str,
        start: usize,
        end: usize,
        tokens: &mut Vec<Token>,
    ) {
        if let Some(last) = tokens.last_mut() {
            // If the whitespace span starts with a literal space, that space is
            // consumed as the previous token's trailing whitespace. Any remaining
            // whitespace becomes a token of its own.
            if span_text.starts_with(' ') {
                last.has_space_after = true;
                if span_text.len() > 1 {
                    tokens.push(Token::new(
                        start + 1,
                        end,
                        span_text[1..].to_string(),
                        false,
                    ));
                }
            } else {
                tokens.push(Token::new(start, end, span_text.to_string(), false));
            }
        } else {
            // Leading whitespace: the whole span becomes a token.
            tokens.push(Token::new(start, end, span_text.to_string(), false));
        }
    }

    /// Tokenize a single whitespace-free span, with caching.
    ///
    /// Offsets in the returned tokens are relative to the start of `text`.
    fn tokenize_span_cached(&self, text: &str, use_special_cases: bool) -> Vec<Token> {
        let key = (text.to_string(), use_special_cases);
        {
            let cache = self.span_cache.lock().unwrap();
            if let Some(tokens) = cache.get(&key) {
                return tokens.clone();
            }
        }
        let tokens = self.tokenize_span_uncached(text, use_special_cases);
        let mut cache = self.span_cache.lock().unwrap();
        if cache.len() < SPAN_CACHE_LIMIT {
            cache.insert(key, tokens.clone());
        }
        tokens
    }

    /// Tokenize a single whitespace-free span.
    ///
    /// Offsets in the returned tokens are relative to the start of `text`.
    fn tokenize_span_uncached(&self, text: &str, use_special_cases: bool) -> Vec<Token> {
        if text.is_empty() {
            return Vec::new();
        }

        let mut prefixes: Vec<Token> = Vec::new();
        let mut suffixes: Vec<Token> = Vec::new();
        let mut current_start: usize = 0;
        let mut current_end: usize = text.len();
        let mut last_size = 0;

        loop {
            let remaining_len = current_end.saturating_sub(current_start);
            if remaining_len == 0 || remaining_len == last_size {
                break;
            }
            last_size = remaining_len;
            let remaining = &text[current_start..current_end];

            if self.matches_token_match(remaining) {
                break;
            }
            if use_special_cases && self.single_special_cases.contains_key(remaining) {
                break;
            }

            let pre_len = self.find_prefix(remaining);
            if pre_len > 0 {
                let prefix_text = remaining[..pre_len].to_string();
                prefixes.push(Token::new(
                    current_start,
                    current_start + pre_len,
                    prefix_text,
                    false,
                ));
                current_start += pre_len;
                let after_prefix = &text[current_start..current_end];
                if use_special_cases && self.single_special_cases.contains_key(after_prefix) {
                    break;
                }
                continue;
            }

            let suf_len = self.find_suffix(remaining);
            if suf_len > 0 {
                let suffix_start = current_end - suf_len;
                let suffix_text = text[suffix_start..current_end].to_string();
                suffixes.push(Token::new(suffix_start, current_end, suffix_text, false));
                current_end -= suf_len;
                let after_suffix = &text[current_start..current_end];
                if use_special_cases && self.single_special_cases.contains_key(after_suffix) {
                    break;
                }
                continue;
            }

            // No prefix or suffix was found; stop to avoid an infinite loop.
            break;
        }

        let mut result = prefixes;
        let remaining = &text[current_start..current_end];
        if !remaining.is_empty() {
            if use_special_cases {
                if let Some(specs) = self.single_special_cases.get(remaining) {
                    let n = specs.len();
                    let mut spec_start = current_start;
                    for (i, spec) in specs.iter().enumerate() {
                        let is_last = i == n - 1;
                        let spec_end = if is_last {
                            current_end
                        } else {
                            spec_start + spec.orth.len()
                        };
                        result.push(Token::new(
                            spec_start,
                            spec_end,
                            spec.orth.clone(),
                            false,
                        ));
                        spec_start = spec_end;
                    }
                } else if self.matches_token_match(remaining) || self.matches_url_match(remaining) {
                    result.push(Token::new(
                        current_start,
                        current_end,
                        remaining.to_string(),
                        false,
                    ));
                } else {
                    result.extend(self.split_infix_with_offsets(remaining, current_start));
                }
            } else if self.matches_token_match(remaining) || self.matches_url_match(remaining) {
                result.push(Token::new(
                    current_start,
                    current_end,
                    remaining.to_string(),
                    false,
                ));
            } else {
                result.extend(self.split_infix_with_offsets(remaining, current_start));
            }
        }
        result.extend(suffixes.into_iter().rev());
        result
    }

    /// Apply multi-token special cases to an already affix-tokenized sequence.
    fn apply_multi_special_cases(&self, tokens: Vec<Token>) -> Vec<Token> {
        let token_texts: Vec<String> = tokens.iter().map(|t| t.text.clone()).collect();
        let mut matches = self.multi_special_cases.find_matches(&token_texts);
        if matches.is_empty() {
            return tokens;
        }

        // Sort by length descending, then start ascending.  Prefer longest,
        // leftmost matches.  Then filter out overlapping matches.
        matches.sort_by(|a, b| {
            let len_a = a.1 - a.0;
            let len_b = b.1 - b.0;
            len_b.cmp(&len_a).then_with(|| a.0.cmp(&b.0))
        });

        let mut seen = vec![false; tokens.len()];
        let mut filtered = Vec::new();
        for (start, end, specs) in matches {
            if seen[start..end].iter().any(|&v| v) {
                continue;
            }
            for i in start..end {
                seen[i] = true;
            }
            filtered.push((start, end, specs));
        }
        filtered.sort_by_key(|m| m.0);

        // Reconstruct the token sequence.
        let mut result = Vec::with_capacity(tokens.len());
        let mut i = 0;
        let mut filtered_iter = filtered.into_iter().peekable();
        while i < tokens.len() {
            if let Some((start, _end, _)) = filtered_iter.peek() {
                if *start == i {
                    let (start, end, specs) = filtered_iter.next().unwrap();
                    let final_spacy = tokens[end - 1].has_space_after;
                    let match_start = tokens[start].start;
                    let match_end = tokens[end - 1].end;
                    let n = specs.len();
                    let mut spec_start = match_start;
                    for (j, spec) in specs.iter().enumerate() {
                        let is_last = j == n - 1;
                        let spec_end = if is_last {
                            match_end
                        } else {
                            spec_start + spec.orth.len()
                        };
                        result.push(Token::new(
                            spec_start,
                            spec_end,
                            spec.orth.clone(),
                            if is_last { final_spacy } else { false },
                        ));
                        spec_start = spec_end;
                    }
                    i = end;
                    continue;
                }
            }
            result.push(tokens[i].clone());
            i += 1;
        }
        result
    }

    fn find_prefix(&self, text: &str) -> usize {
        match self.prefix_re.find(text) {
            Ok(Some(m)) if m.start() == 0 => m.end() - m.start(),
            _ => 0,
        }
    }

    fn find_suffix(&self, text: &str) -> usize {
        // The suffix regex is anchored with `$`, so the first match is at the end.
        match self.suffix_re.find(text) {
            Ok(Some(m)) if m.end() == text.len() => m.end() - m.start(),
            _ => 0,
        }
    }

    fn matches_token_match(&self, text: &str) -> bool {
        self.token_match
            .as_ref()
            .map(|re| matches!(re.find(text), Ok(Some(m)) if m.start() == 0))
            .unwrap_or(false)
    }

    fn matches_url_match(&self, text: &str) -> bool {
        self.url_match
            .as_ref()
            .map(|re| matches!(re.find(text), Ok(Some(m)) if m.start() == 0))
            .unwrap_or(false)
    }

    fn split_infix_with_offsets(&self, text: &str, base_offset: usize) -> Vec<Token> {
        let mut matches = Vec::new();
        for m in self.infix_re.find_iter(text) {
            match m {
                Ok(m) => matches.push(m),
                Err(_) => continue,
            }
        }

        if matches.is_empty() {
            return vec![Token::new(
                base_offset,
                base_offset + text.len(),
                text.to_string(),
                false,
            )];
        }

        let mut result = Vec::new();
        let mut start = 0;
        for m in matches {
            if m.start() != start {
                result.push(Token::new(
                    base_offset + start,
                    base_offset + m.start(),
                    text[start..m.start()].to_string(),
                    false,
                ));
            }
            if m.start() != m.end() {
                result.push(Token::new(
                    base_offset + m.start(),
                    base_offset + m.end(),
                    text[m.start()..m.end()].to_string(),
                    false,
                ));
            }
            start = m.end();
        }
        if start < text.len() {
            result.push(Token::new(
                base_offset + start,
                base_offset + text.len(),
                text[start..].to_string(),
                false,
            ));
        }
        result
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn english_tokenizer() -> Tokenizer {
        let rules = SpaCyRules::english_defaults();
        Tokenizer::from_spacy_rules(&rules).unwrap()
    }

    #[test]
    fn test_basic_tokenization() {
        let tok = english_tokenizer();
        let tokens = tok.tokenize_texts("Hello, world!");
        assert_eq!(tokens, vec!["Hello", ",", "world", "!"]);
    }

    #[test]
    fn test_contraction() {
        let tok = english_tokenizer();
        let tokens = tok.tokenize_texts("I don't know.");
        assert_eq!(tokens, vec!["I", "do", "n't", "know", "."]);
    }

    #[test]
    fn test_url() {
        let tok = english_tokenizer();
        let tokens = tok.tokenize_texts("Visit https://example.com today.");
        assert_eq!(
            tokens,
            vec!["Visit", "https://example.com", "today", "."]
        );
    }

    #[test]
    fn test_punctuation_spacing() {
        let tok = english_tokenizer();
        let tokens = tok.tokenize("Hello, world!");
        assert_eq!(tokens[0].has_space_after, false); // Hello
        assert_eq!(tokens[1].has_space_after, true);  // ,
        assert_eq!(tokens[2].has_space_after, false); // world
        assert_eq!(tokens[3].has_space_after, false); // !
    }
}
