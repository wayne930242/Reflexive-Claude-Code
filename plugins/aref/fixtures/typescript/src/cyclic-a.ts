import { bFn } from './cyclic-b';

export function aFn(n: number): number {
  if (n <= 0) return 0;
  return bFn(n - 1) + 1;
}
