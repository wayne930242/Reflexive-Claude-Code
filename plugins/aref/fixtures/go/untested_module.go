package fixture

// Intentionally untested module for aref self-testing.
// aref's scaffolding-characterization-tests should mark this must-scaffold.

func ComputePriorityScore(severity int, impact int, confidence float64) int {
	raw := float64(severity) * float64(impact) * confidence
	if raw > 100 {
		return 100
	}
	if raw < 0 {
		return 0
	}
	return int(raw + 0.5)
}
