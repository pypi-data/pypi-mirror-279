from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.type import forall

__all__ = (
    'Maybe',
    'Nothing',
    'Just',
)


a = TypeVar('a')


@dataclass(frozen=True)
class Nothing: ...


@dataclass(frozen=True)
class Just(forall[a]):
    x : a


Maybe = Nothing | Just[a]
