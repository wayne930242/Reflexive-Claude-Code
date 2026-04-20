// This module has no tests. aref should mark it must-scaffold.

export function computePriorityScore(input: {
  severity: number;
  impact: number;
  confidence: number;
}): number {
  const raw = input.severity * input.impact * input.confidence;
  if (raw > 100) return 100;
  if (raw < 0) return 0;
  return Math.round(raw);
}
