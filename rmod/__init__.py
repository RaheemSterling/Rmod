from .model import S5Model, Formula
from .checker import evaluate, satisfies, satisfies_somewhere
from .distance import quotient_distance
from .partition import enumerate_partitions, bell_number
from .algorithms import rmod_exhaustive, rmod_vfixed, rmod_single_class

__version__ = '0.1.0'

__all__ = [
    'S5Model',
    'Formula',
    'evaluate',
    'satisfies',
    'satisfies_somewhere',
    'quotient_distance',
    'enumerate_partitions',
    'bell_number',
    'rmod_exhaustive',
    'rmod_vfixed',
    'rmod_single_class',
]
