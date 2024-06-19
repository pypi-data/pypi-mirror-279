from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.type import Lambda, forall

__all__ = (
    'Endo',
    'appEndo',
)


a = TypeVar('a')


@dataclass(frozen=True)
class Endo(forall[a]):
    appEndo : Lambda[a, a]


def appEndo(x : Endo[a], /) -> Lambda[a, a]:
    match x:
        case Endo(appEndo):
            return appEndo
