//! Intentionally untested module for aref self-testing.
//! aref's scaffolding-characterization-tests should mark this must-scaffold.

pub fn compute_priority_score(severity: i32, impact: i32, confidence: f64) -> i32 {
    let raw = severity as f64 * impact as f64 * confidence;
    if raw > 100.0 {
        return 100;
    }
    if raw < 0.0 {
        return 0;
    }
    raw.round() as i32
}
