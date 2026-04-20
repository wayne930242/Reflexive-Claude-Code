//! Rust prevents module cycles at compile time but workspace crate cycles are possible.
//! For single-crate fixture we simulate a cycle through mutual recursion between modules
//! via a shared module boundary.

pub mod alpha {
    use super::beta;

    pub fn a_fn(n: i32) -> i32 {
        if n <= 0 { return 0; }
        beta::b_fn(n - 1) + 1
    }
}

pub mod beta {
    use super::alpha;

    pub fn b_fn(n: i32) -> i32 {
        if n <= 0 { return 0; }
        alpha::a_fn(n - 1) + 2
    }
}
