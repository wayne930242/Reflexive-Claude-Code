from src.cyclic_a import a_fn


def b_fn(n: int) -> int:
    if n <= 0:
        return 0
    return a_fn(n - 1) + 2
