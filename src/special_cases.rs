use crate::rules::SpaCyRuleSpec;
use std::collections::HashMap;

/// A trie that maps sequences of token texts onto special-case output specs.
///
/// This is used for spaCy-style multi-token special cases (e.g. a key that
/// affix-tokenizes into more than one token).  Matching is performed by
/// walking the trie from every start position in the token sequence.
#[derive(Debug, Default)]
pub struct TokenSequenceTrie {
    root: TrieNode,
}

#[derive(Debug, Default)]
struct TrieNode {
    /// Child nodes keyed by the next token text.
    children: HashMap<String, TrieNode>,
    /// If this node is the end of a key, the output spec sequence.
    value: Option<Vec<SpaCyRuleSpec>>,
}

impl TokenSequenceTrie {
    pub fn new() -> Self {
        Self::default()
    }

    /// Insert a key sequence and its output spec.
    pub fn insert(&mut self, key: Vec<String>, value: Vec<SpaCyRuleSpec>) {
        let mut node = &mut self.root;
        for token in key {
            node = node.children.entry(token).or_default();
        }
        node.value = Some(value);
    }

    /// Find all matches in `tokens` and return them as `(start, end, value)`
    /// triples.  Matches are not overlapping in the sense that each starting
    /// index is only reported once, taking the longest match at that position.
    ///
    /// The returned matches are sorted by start index.
    pub fn find_matches(&self, tokens: &[String]) -> Vec<(usize, usize, Vec<SpaCyRuleSpec>)> {
        let mut matches = Vec::new();
        for start in 0..tokens.len() {
            let mut node = &self.root;
            let mut end = start;
            for i in start..tokens.len() {
                match node.children.get(&tokens[i]) {
                    Some(child) => {
                        node = child;
                        end = i + 1;
                        if node.value.is_some() {
                            // We keep walking so the longest match wins.
                        }
                    }
                    None => break,
                }
            }
            if let Some(value) = node.value.as_ref() {
                matches.push((start, end, value.clone()));
            }
        }
        matches
    }
}

