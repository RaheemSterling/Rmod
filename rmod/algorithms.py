import time
import itertools
from typing import List, Tuple, Optional

from .model import S5Model, Formula
from .checker import evaluate, satisfies_somewhere
from .distance import quotient_distance
from .partition import enumerate_partitions


def rmod_exhaustive(M: S5Model, phi: Formula, timeout: float = 600.0) -> Tuple[List[S5Model], int, float]:
    start = time.time()
    atoms = phi.atoms()
    k = len(atoms)
    atom_list = sorted(atoms)

    best_dist = float('inf')
    minimizers = []

    for part in enumerate_partitions(M.n):
        for val_bits in itertools.product([0, 1], repeat=k * M.n):
            if time.time() - start > timeout:
                return minimizers, best_dist, timeout

            valuation = {}
            for i, atom in enumerate(atom_list):
                valuation[atom] = {w for w in range(M.n) if val_bits[i * M.n + w]}

            M_prime = S5Model(n=M.n, partition=[c.copy() for c in part], valuation=valuation)

            if not satisfies_somewhere(M_prime, phi):
                continue

            dist = quotient_distance(M, M_prime, atoms)

            if dist < best_dist:
                best_dist = dist
                minimizers = [M_prime]
            elif dist == best_dist:
                minimizers.append(M_prime)

    elapsed = time.time() - start
    return minimizers, best_dist if best_dist != float('inf') else -1, elapsed


def rmod_vfixed(M: S5Model, phi: Formula, timeout: float = 600.0) -> Tuple[List[S5Model], int, float]:
    start = time.time()
    atoms = phi.atoms()

    best_dist = float('inf')
    minimizers = []

    for part in enumerate_partitions(M.n):
        if time.time() - start > timeout:
            return minimizers, best_dist, timeout

        M_prime = S5Model(
            n=M.n,
            partition=[c.copy() for c in part],
            valuation={k: v.copy() for k, v in M.valuation.items()}
        )

        if not satisfies_somewhere(M_prime, phi):
            continue

        dist = quotient_distance(M, M_prime, atoms)

        if dist < best_dist:
            best_dist = dist
            minimizers = [M_prime]
        elif dist == best_dist:
            minimizers.append(M_prime)

    elapsed = time.time() - start
    return minimizers, best_dist if best_dist != float('inf') else -1, elapsed


def rmod_single_class(M: S5Model, phi: Formula) -> Tuple[Optional[S5Model], int, float]:
    start = time.time()
    atoms = phi.atoms()

    offending_class = None
    for cls in M.partition:
        for w in cls:
            if not evaluate(M, phi, w):
                offending_class = cls
                break
        if offending_class:
            break

    if offending_class is None:
        return M.copy(), 0, time.time() - start

    best_dist = float('inf')
    best_model = None

    for u in offending_class:
        new_partition = []
        for cls in M.partition:
            if cls is offending_class:
                if len(cls) > 1:
                    new_partition.append({u})
                    new_partition.append(cls - {u})
                else:
                    new_partition.append(cls.copy())
            else:
                new_partition.append(cls.copy())

        M_prime = S5Model(
            n=M.n,
            partition=new_partition,
            valuation={k: v.copy() for k, v in M.valuation.items()}
        )

        if satisfies_somewhere(M_prime, phi):
            dist = quotient_distance(M, M_prime, atoms)
            if dist < best_dist:
                best_dist = dist
                best_model = M_prime

    for other_cls in M.partition:
        if other_cls is offending_class:
            continue

        new_partition = []
        merged = offending_class | other_cls
        for cls in M.partition:
            if cls is offending_class or cls is other_cls:
                continue
            new_partition.append(cls.copy())
        new_partition.append(merged)

        M_prime = S5Model(
            n=M.n,
            partition=new_partition,
            valuation={k: v.copy() for k, v in M.valuation.items()}
        )

        if satisfies_somewhere(M_prime, phi):
            dist = quotient_distance(M, M_prime, atoms)
            if dist < best_dist:
                best_dist = dist
                best_model = M_prime

    elapsed = time.time() - start
    return best_model, best_dist if best_model else -1, elapsed
