from __future__ import annotations

from typing import TypeVar

from categories.type import Lambda

__all__ = (
    'Parser',
)


a = TypeVar('a')


Parser = Lambda[str, list[tuple[a, str]]]
