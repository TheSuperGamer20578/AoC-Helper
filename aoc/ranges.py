def irange(a: int, b: int, step: int = 1) -> range:
    """Inclusive range"""
    return range(a, b + 1, step)


def srange(a: int, b: int, step: int = 1) -> range | None:
    """Smart range
    range(a, b, step) if a < b
    range(a, b, -step) if a > b
    None if a == b
    """
    if a < b:
        return range(a, b, step)
    if a > b:
        return range(a, b, -step)
    return None


def sirange(a: int, b: int, step: int = 1) -> range | None:
    """Smart inclusive range"""
    return srange(a, b + 1, step)
