import { aFn } from './cyclic-a';

export function bFn(n: number): number {
  if (n <= 0) return 0;
  return aFn(n - 1) + 2;
}
