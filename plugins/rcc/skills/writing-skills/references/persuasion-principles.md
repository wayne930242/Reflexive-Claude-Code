# Persuasion Principles for Skill Design

## Overview

LLMs respond to the same persuasion principles as humans. Understanding this helps design skills that are followed even under pressure.

**Research:** Meincke et al. (2025) tested persuasion with N=28,000 AI conversations. Compliance increased from 33% to 72% with persuasion techniques.

## Key Principles for Skills

### 1. Authority

**What:** Deference to expertise and official sources.

**In skills:**
- Imperative language: "YOU MUST", "NEVER", "No exceptions"
- Eliminates rationalization space

**When to use:** Discipline-enforcing skills (TDD, verification requirements)

```markdown
✅ Write code before test? Delete it. Start over. No exceptions.
❌ Consider writing tests first when feasible.
```

### 2. Commitment

**What:** Consistency with prior declarations.

**In skills:**
- Require announcements: "Announce skill usage"
- Force explicit choices: "Choose A, B, or C"
- Use TaskCreate for tracking

**When to use:** Multi-step processes, accountability

```markdown
✅ TaskCreate for EACH step. TaskUpdate when complete.
❌ Keep track of your progress mentally.
```

### 3. Social Proof

**What:** Conformity to what's normal.

**In skills:**
- Universal patterns: "Every time", "Always"
- Failure modes: "X without Y = failure"

**When to use:** Documenting universal practices

```markdown
✅ Skills without baseline testing = weak skills. Every time.
❌ Some people find baseline testing helpful.
```

### 4. Scarcity

**What:** Urgency from time limits.

**In skills:**
- Time-bound: "Before proceeding"
- Sequential: "Immediately after X"

**When to use:** Preventing "I'll do it later"

```markdown
✅ After completing task, IMMEDIATELY run validation.
❌ Validate when convenient.
```

## Principle Combinations

| Skill Type | Use | Avoid |
|------------|-----|-------|
| Discipline-enforcing | Authority + Commitment + Social Proof | Liking |
| Guidance/technique | Moderate Authority | Heavy authority |
| Reference | Clarity only | All persuasion |

## Why This Works

**Bright-line rules reduce rationalization:**
- "YOU MUST" removes decision fatigue
- Absolute language eliminates "is this an exception?"

**Implementation intentions:**
- "When X, do Y" more effective than "generally do Y"
- Clear triggers + required actions = automatic execution

## Ethical Use

**Legitimate:**
- Ensuring critical practices followed
- Preventing predictable failures

**Test:** Would this serve the user's genuine interests if they fully understood it?

## Citation

Meincke, L., Shapiro, D., Duckworth, A. L., Mollick, E., Mollick, L., & Cialdini, R. (2025). *Call Me A Jerk: Persuading AI to Comply with Objectionable Requests.* University of Pennsylvania.
