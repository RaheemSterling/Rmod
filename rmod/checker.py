from .model import S5Model, Formula


def evaluate(M: S5Model, phi: Formula, w: int) -> bool:
    if phi.op == 'atom':
        return w in M.valuation.get(phi.atom, set())
    elif phi.op == 'neg':
        return not evaluate(M, phi.sub, w)
    elif phi.op == 'and':
        return evaluate(M, phi.left, w) and evaluate(M, phi.right, w)
    elif phi.op == 'or':
        return evaluate(M, phi.left, w) or evaluate(M, phi.right, w)
    elif phi.op == 'box':
        cls = M.get_class(w)
        return all(evaluate(M, phi.sub, v) for v in cls)
    elif phi.op == 'diamond':
        cls = M.get_class(w)
        return any(evaluate(M, phi.sub, v) for v in cls)
    raise ValueError(f"Unknown operator: {phi.op}")


def satisfies(M: S5Model, phi: Formula) -> bool:
    return all(evaluate(M, phi, w) for w in range(M.n))


def satisfies_somewhere(M: S5Model, phi: Formula) -> bool:
    return any(evaluate(M, phi, w) for w in range(M.n))
