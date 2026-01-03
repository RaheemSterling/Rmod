from dataclasses import dataclass
from typing import List, Set, Dict, Optional


@dataclass
class S5Model:
    n: int
    partition: List[Set[int]]
    valuation: Dict[str, Set[int]]

    def get_class(self, w: int) -> Set[int]:
        for cls in self.partition:
            if w in cls:
                return cls
        raise ValueError(f"World {w} not in any class")

    def copy(self) -> 'S5Model':
        return S5Model(
            n=self.n,
            partition=[cls.copy() for cls in self.partition],
            valuation={k: v.copy() for k, v in self.valuation.items()}
        )


@dataclass
class Formula:
    op: str
    atom: Optional[str] = None
    sub: Optional['Formula'] = None
    left: Optional['Formula'] = None
    right: Optional['Formula'] = None

    def __repr__(self):
        if self.op == 'atom':
            return self.atom
        elif self.op == 'neg':
            return f"¬{self.sub}"
        elif self.op == 'and':
            return f"({self.left} ∧ {self.right})"
        elif self.op == 'or':
            return f"({self.left} ∨ {self.right})"
        elif self.op == 'box':
            return f"□{self.sub}"
        elif self.op == 'diamond':
            return f"◇{self.sub}"
        return f"Formula({self.op})"

    def atoms(self) -> Set[str]:
        if self.op == 'atom':
            return {self.atom}
        elif self.op in ('neg', 'box', 'diamond'):
            return self.sub.atoms()
        elif self.op in ('and', 'or'):
            return self.left.atoms() | self.right.atoms()
        return set()
