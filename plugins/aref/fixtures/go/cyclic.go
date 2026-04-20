package fixture

// CyclicAlpha calls CyclicBeta which calls CyclicAlpha.
// Single-package mutual recursion substitutes for inter-package cycle
// in this minimal fixture. Multi-package fixture is out of scope for v0.1.
func CyclicAlpha(n int) int {
	if n <= 0 {
		return 0
	}
	return CyclicBeta(n-1) + 1
}

func CyclicBeta(n int) int {
	if n <= 0 {
		return 0
	}
	return CyclicAlpha(n-1) + 2
}
