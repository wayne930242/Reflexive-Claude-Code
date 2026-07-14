---
name: reflecting
description: Scans the session, suggests what is worth reflecting on, and lets the user pick which learnings to deepen. Use when completing significant work, when the user corrects your approach, when a bug is resolved, or when new patterns emerge. Use when user says "reflect", "what did we learn", "capture learnings".
argument-hint: "[pain-point]"
---

# Reflecting

## Overview

**Reflecting IS surfacing candidate learnings, then deepening only the ones the user picks.**

Scan the session, list what is *worth* reflecting on with a one-line reason each, and let the user choose.
Do not force every event into a full learning report.
Capture before context fades; deepen on demand.

**When to reflect:** after a significant feature, a resolved bug, repeated failed attempts, an unexpected discovery, or a long session.
Don't wait for "later" — context fades fast.

## Routing

**Pattern:** suggest → pick → deepen
**Hand off:** `planning-agent-systems`, opt-in (only when a learning should become a component)

## Stage 1: Suggest Candidates (lightweight)

Scan the conversation for moments worth reflecting on.
For each, write ONE line:

`[type] short description — why it's worth a look`

Types: **correction** (user corrected you), **error** (mistake / multiple attempts), **discovery** (new insight about project/domain/tooling), **repetition** (same action repeated — automation candidate), **safety_bypass** (destructive/irreversible action without confirmation, or a safety check skipped).

Rules:

- No minimum count. A quiet session may yield one candidate, or none. One honest candidate beats a forced three.
- Do NOT trace routers, locate files, or fill multi-field forms here. Stage 1 is a menu, not a report.
- **safety_bypass is always surfaced, flagged ⚠️** — never bury a skipped safety check, even in a light scan. Watch for: `--force` / `reset --hard` / `clean -f` / `branch -D`, `--no-verify`, `rm -rf` / dropping tables, deleting or editing tests to pass, discarding unfamiliar files, `rsync --delete` without exclusions, or user interjections ("stop", "don't", "wait", "undo", "rollback").
- If a pain point was given via `$ARGUMENTS`, list it first — even if the trace doesn't show it failing.

Present the list and ask: **which do you want to deepen?** (some, all, or none.)

## Stage 2: Deepen Picked Candidates only

For each candidate the user picks:

1. **Extract the learning** — what would prevent the failure or repeat the success, and where it applies.
2. **Locate the router** — which skill/rule/law/CLAUDE.md routed the behavior. Glob the path; "none" if it came from general knowledge.
3. **Suggest where the fix lands** — simplest component that works:
   - one-line convention → `rule`; immutable project constraint → `law`; repeated multi-step process → `skill`; automated check → `hook`; reference material → `doc`
   - **safety_bypass → `rule` or `law` only** — never a skill alone (safety needs always-on enforcement). Name the exact command/flag to block.
4. **Debug session** — capture two things separately: the bug itself (root cause + prevention rule) and any reasoning error made while debugging.

Write the picked learnings to `.rcc/{YYYY-MM-DD}-reflection.md` using `references/report-template.md`.

## Stage 3: Land (optional)

Default: present the suggested fixes; let the user apply them.

To turn a learning into a component automatically, hand off to `planning-agent-systems` with the reflection path.
Otherwise stop — do not auto-create components.

## Red Flags — STOP

- "Surface everything as a full learning" → Stage 1 is a menu; only deepen the picks.
- "Skip the safety_bypass — user didn't complain" → silence ≠ consent. Always surface it, flagged.
- "Auto-create the component, I know where it goes" → landing is opt-in. Suggest, don't impose.
- "Nothing worth noting" → scan once more; capture now, context fades.

## References

- `references/report-template.md` — lightweight reflection list format
- `planning-agent-systems` — opt-in, only when turning a learning into a component
- `.rcc/config.yml` `decisions_log` — append new decisions here
