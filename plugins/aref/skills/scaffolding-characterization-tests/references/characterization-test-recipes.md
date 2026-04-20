# Characterization Test Recipes

Per-language patterns for capturing current behavior as golden output.

## TypeScript / JavaScript

Library: `vitest` (preferred) or `jest`. For snapshots: built-in `toMatchSnapshot` or `@vitest/snapshot`.

```ts
import { describe, it, expect } from 'vitest';
import { targetFunction } from '../src/target';

describe('targetFunction — characterization', () => {
  it('captures behavior for input A', () => {
    expect(targetFunction(inputA)).toMatchSnapshot();
  });
  it('captures behavior for input B', () => {
    expect(targetFunction(inputB)).toMatchSnapshot();
  });
});
```

Inputs from call-site samples. Commit `__snapshots__/` directory.

## Python

Library: `pytest` + `syrupy` (snapshot plugin).

```python
def test_target_characterization_input_a(snapshot):
    from src.target import target_function
    assert target_function(INPUT_A) == snapshot
```

Install: `pip install syrupy`. Commit `__snapshots__/` directories.

## Rust

Library: `insta`.

```rust
use insta::assert_snapshot;

#[test]
fn target_function_input_a() {
    let result = my_crate::target_function(input_a());
    assert_snapshot!(result);
}
```

Install: `cargo add --dev insta`. Commit `snapshots/` directories.

## Go

Library: `github.com/stretchr/testify` + golden files.

```go
func TestTargetFunction_InputA(t *testing.T) {
    result := TargetFunction(inputA)
    golden := filepath.Join("testdata", "target_input_a.golden")
    if *update {
        os.WriteFile(golden, []byte(result), 0644)
    }
    expected, _ := os.ReadFile(golden)
    assert.Equal(t, string(expected), result)
}
```

Use `-update` flag on first run to capture; subsequent runs assert.

## High-Risk Markers

Skip scaffold and escalate to user if module:
- Makes network calls
- Reads/writes files at arbitrary paths
- Depends on system time / PID / randomness without seed injection
- Calls subprocesses
- Depends on specific hardware

Escalation message template:
> Module `<path>` is high-risk for characterization testing (reason: `<reason>`). Options: (1) introduce a seam to inject the side-effect source, adding a pre-refactor seam phase; (2) accept risk and proceed without scaffold; (3) drop this module from the plan. Pick one.
