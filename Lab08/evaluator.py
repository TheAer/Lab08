"""Чисті функції обчислення та підстановки змінних через match/case (Варіант 3)."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from model import Add, Expr, Mul, Num, Var

MAX_ABS: Final[int] = 1_000_000


class EvalError(Exception):
    """Базовий виняток обчислювача алгебраїчних виразів."""


class UndefinedVariableError(EvalError, KeyError):
    """Виняток при зверненні до змінної, відсутньої у середовищі env."""

    def __init__(self, var_name: str) -> None:
        self.var_name = var_name
        super().__init__(f"Змінну '{var_name}' не знайдено у середовищі обчислення.")


class EvalOverflowError(EvalError, OverflowError):
    """Виняток при виході проміжного або кінцевого результату за допустимі межі."""


def _check_bounds(value: int) -> int:
    if abs(value) > MAX_ABS:
        raise EvalOverflowError(f"Переповнення допустимого діапазону: {value}")
    return value


def eval_expr(expr: Expr, env: Mapping[str, int] | None = None) -> int:
    """Чисто обчислює значення виразу Expr у середовищі змінних env через match/case."""
    scope: Mapping[str, int] = {} if env is None else env
    match expr:
        case Num(value=v):
            return _check_bounds(v)
        case Var(name=name):
            if name not in scope:
                raise UndefinedVariableError(name)
            return _check_bounds(scope[name])
        case Add(left=left, right=right):
            return _check_bounds(eval_expr(left, scope) + eval_expr(right, scope))
        case Mul(left=left, right=right):
            return _check_bounds(eval_expr(left, scope) * eval_expr(right, scope))


def substitute(expr: Expr, env: Mapping[str, int]) -> Expr:
    """Повертає нове незмінне дерево Expr із підставленими значеннями відомих змінних."""
    match expr:
        case Num():
            return expr
        case Var(name=name):
            return Num(env[name]) if name in env else expr
        case Add(left=left, right=right):
            return Add(substitute(left, env), substitute(right, env))
        case Mul(left=left, right=right):
            return Mul(substitute(left, env), substitute(right, env))


def collect_variables(expr: Expr) -> frozenset[str]:
    """Повертає множину імен усіх змінних, що зустрічаються у виразі Expr."""
    match expr:
        case Num():
            return frozenset()
        case Var(name=name):
            return frozenset({name})
        case Add(left=left, right=right) | Mul(left=left, right=right):
            return collect_variables(left) | collect_variables(right)
