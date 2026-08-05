#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Token {
    /// Byte offset where the token starts in the original text.
    pub start: usize,
    /// Byte offset where the token ends in the original text.
    pub end: usize,
    /// Token text.
    pub text: String,
    /// Whether the token is followed by a space in the original text.
    pub has_space_after: bool,
}

impl Token {
    pub fn new(start: usize, end: usize, text: String, has_space_after: bool) -> Self {
        Self {
            start,
            end,
            text,
            has_space_after,
        }
    }
}
