from typing import Set
from .model import S5Model


def quotient_distance(M1: S5Model, M2: S5Model, atoms: Set[str]) -> int:
    struct_dist = 0
    for i in range(M1.n):
        for j in range(i + 1, M1.n):
            same_class_1 = any(i in cls and j in cls for cls in M1.partition)
            same_class_2 = any(i in cls and j in cls for cls in M2.partition)
            if same_class_1 != same_class_2:
                struct_dist += 1

    val_dist = 0
    for atom in atoms:
        v1 = M1.valuation.get(atom, set())
        v2 = M2.valuation.get(atom, set())
        val_dist += len(v1.symmetric_difference(v2))

    return struct_dist + val_dist
