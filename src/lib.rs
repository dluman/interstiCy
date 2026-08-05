use pyo3::prelude::*;
use pyo3::types::PyList;
use rayon::prelude::*;

mod rules;
mod special_cases;
mod token;
mod tokenizer;

use rules::SpaCyRules;
use tokenizer::Tokenizer as InnerTokenizer;

/// A spaCy-compatible tokenizer implemented in Rust.
#[pyclass(name = "Tokenizer")]
pub struct PyTokenizer {
    inner: InnerTokenizer,
}

#[pymethods]
impl PyTokenizer {
    /// Load default English tokenizer rules from spaCy.
    #[staticmethod]
    fn load_from_spacy(_py: Python<'_>) -> PyResult<Self> {
        let rules = SpaCyRules::english_defaults();
        let inner = InnerTokenizer::from_spacy_rules(&rules)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("{e}")))?;
        Ok(Self { inner })
    }

    /// Tokenize text and return a list of token strings.
    fn tokenize<'py>(&self, py: Python<'py>, text: &str) -> PyResult<Bound<'py, PyList>> {
        let tokens = self.inner.tokenize_texts(text);
        let list = PyList::new(py, tokens)?;
        Ok(list)
    }

    /// Tokenize text and return a list of `(start_char, end_char, text, has_space_after)` tuples.
    fn tokenize_with_spans<'py>(
        &self,
        py: Python<'py>,
        text: &str,
    ) -> PyResult<Bound<'py, PyList>> {
        let offset_map = build_byte_to_char_map(text);
        let tokens = self
            .inner
            .tokenize(text)
            .into_iter()
            .map(|t| (offset_map[t.start], offset_map[t.end], t.text, t.has_space_after));
        let list = PyList::new(py, tokens)?;
        Ok(list)
    }

    /// Tokenize a list of texts in parallel and return a list of
    /// `(start_char, end_char, text, has_space_after)` tuples per text.
    ///
    /// The GIL is released while the tokenization runs, so other Python threads
    /// can execute concurrently.
    fn tokenize_with_spans_batch<'py>(
        &self,
        py: Python<'py>,
        texts: Vec<String>,
    ) -> PyResult<Bound<'py, PyList>> {
        let results: Vec<Vec<(usize, usize, String, bool)>> = py.detach(|| {
            texts
                .par_iter()
                .map(|text| {
                    let offset_map = build_byte_to_char_map(text);
                    self.inner
                        .tokenize(text)
                        .into_iter()
                        .map(|t| {
                            (
                                offset_map[t.start],
                                offset_map[t.end],
                                t.text,
                                t.has_space_after,
                            )
                        })
                        .collect()
                })
                .collect()
        });

        let outer = PyList::empty(py);
        for inner in results {
            let inner_list = PyList::new(py, inner)?;
            outer.append(inner_list)?;
        }
        Ok(outer)
    }

    /// Tokenize text and return a list of `(text, has_space_after)` tuples.
    fn tokenize_with_spaces<'py>(
        &self,
        py: Python<'py>,
        text: &str,
    ) -> PyResult<Bound<'py, PyList>> {
        let tokens = self
            .inner
            .tokenize(text)
            .into_iter()
            .map(|t| (t.text, t.has_space_after));
        let list = PyList::new(py, tokens)?;
        Ok(list)
    }
}

/// Build a map from byte offset to character offset.
fn build_byte_to_char_map(text: &str) -> Vec<usize> {
    let mut map = vec![0; text.len() + 1];
    let mut char_offset = 0;
    for (byte_offset, _) in text.char_indices() {
        map[byte_offset] = char_offset;
        char_offset += 1;
    }
    map[text.len()] = char_offset;
    map
}

#[pymodule]
fn _intersticy(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyTokenizer>()?;
    Ok(())
}
