from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.type import forall

__all__ = (
    'Dual',
    'getDual',
)


a = TypeVar('a')


@dataclass(frozen=True)
class Dual(forall[a]):
    getDual : a


def getDual(x : Dual[a], /) -> a:
    match x:
        case Dual(getDual):
            return getDual
