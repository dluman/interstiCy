use serde::Deserialize;
use std::collections::HashMap;

const SPACY_RULES_JSON: &str = include_str!("../scripts/spacy_rules.json");

#[derive(Debug, Deserialize)]
pub struct SpaCyRules {
    pub prefix: Option<String>,
    pub suffix: Option<String>,
    pub infix: Option<String>,
    pub token_match: Option<String>,
    pub url_match: Option<String>,
    #[allow(dead_code)]
    pub faster_heuristics: bool,
    pub rules: HashMap<String, Vec<SpaCyRuleSpec>>,
}

#[derive(Debug, Deserialize, Clone)]
pub struct SpaCyRuleSpec {
    #[serde(rename = "ORTH")]
    pub orth: String,
    #[serde(rename = "NORM", default)]
    #[allow(dead_code)]
    pub norm: Option<String>,
}

impl SpaCyRules {
    pub fn english_defaults() -> Self {
        serde_json::from_str(SPACY_RULES_JSON).expect("embedded spaCy rules are valid JSON")
    }
}
