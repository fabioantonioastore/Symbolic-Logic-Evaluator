def disjunction(a: bool, b: bool) -> bool:
    return a or b


def conjunction(a: bool, b: bool) -> bool:
    return a and b


def conditional(a: bool, b: bool) -> bool:
    return not a or b


def biconditional(a: bool, b: bool) -> bool:
    return conditional(a, b) and conditional(b, a)


def negation(a: bool) -> bool:
    return not a
