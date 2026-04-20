from src.cyclic_b import b_fn


def a_fn(n: int) -> int:
    if n <= 0:
        return 0
    return b_fn(n - 1) + 1
