from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from categories.control.monad import Monad
from categories.type import Lambda, hkt, typeclass

__all__ = (
    'MonadFix',
)


a = TypeVar('a')

m = TypeVar('m')


@dataclass(frozen=True)
class MonadFix(Monad[m], typeclass[m]):
    def fix(self, f : Lambda[a, hkt[m, a]], /) -> hkt[m, a]: ...
