# R-Mod

Minimal structural revision operator for S5 epistemic models.

## Installation

```bash
pip install -e .
```

Or simply copy the `rmod` folder to your project.

## Usage

```python
from rmod import S5Model, Formula, rmod_exhaustive, rmod_vfixed, rmod_single_class

M = S5Model(
    n=4,
    partition=[{0, 1}, {2, 3}],
    valuation={'p': {0, 2}, 'q': {1, 2, 3}}
)

phi = Formula(
    op='diamond',
    sub=Formula(
        op='and',
        left=Formula(op='atom', atom='p'),
        right=Formula(op='atom', atom='q')
    )
)

minimizers, distance, elapsed = rmod_exhaustive(M, phi, timeout=60.0)
print(f"Found {len(minimizers)} minimizer(s) at distance {distance}")
```

## Algorithms

| Algorithm | Time Complexity | Completeness |
|-----------|-----------------|--------------|
| `rmod_exhaustive` | O(B(n) · 2^{kn} · poly) | Yes |
| `rmod_vfixed` | O(B(n) · poly) | Yes (valuation fixed) |
| `rmod_single_class` | O(n³ + \|α\|n) | No |

Where B(n) is the n-th Bell number and k is the number of atoms.

## Module Structure

```
rmod/
├── __init__.py      # Package exports
├── model.py         # S5Model, Formula
├── checker.py       # Model checking
├── distance.py      # Quotient distance
├── partition.py     # Partition enumeration
└── algorithms.py    # R-Mod operators
```

## License

MIT
