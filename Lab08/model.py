"""Алгебраїчні типи даних (ADT) для калькулятора зі змінними (Лабораторна №8, Варіант 3)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, TypeAlias, Union

RenderStyle: TypeAlias = Literal["infix", "prefix"]


@dataclass(frozen=True)
class Num:
    """Числовий літерал у синтаксичному дереві виразу."""

    value: int


@dataclass(frozen=True)
class Var:
    """Іменована змінна у синтаксичному дереві виразу."""

    name: str

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Ім'я змінної не може бути порожнім.")


@dataclass(frozen=True)
class Add:
    """Вузол бінарного додавання двох підвиразів."""

    left: Expr
    right: Expr


@dataclass(frozen=True)
class Mul:
    """Вузол бінарного множення двох підвиразів."""

    left: Expr
    right: Expr


Expr: TypeAlias = Union[Num, Var, Add, Mul]


class SupportsRender(Protocol):
    """Структурний контракт для об'єктів, які підтримують текстове форматування."""

    def render(self, style: RenderStyle = "infix") -> str: ...
