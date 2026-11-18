"""Модульні pytest-тести для лабораторної роботи №8 (Варіант 3: Калькулятор зі змінними)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from evaluator import (
    EvalOverflowError,
    UndefinedVariableError,
    collect_variables,
    eval_expr,
    substitute,
)
from model import Add, Expr, Mul, Num, Var
from pretty import RenderableExpr, format_via_protocol, render


def test_atomic_nodes_and_immutability() -> None:
    """Перевіряє Num, Var та незмінність вузлів ADT (frozen=True)."""
    n = Num(42)
    x = Var("x")
    assert eval_expr(n) == 42
    assert eval_expr(x, {"x": -7}) == -7

    with pytest.raises(FrozenInstanceError):
        n.value = 10  # type: ignore[misc]

    with pytest.raises(ValueError):
        Var("   ")


def test_nested_expression_eval_and_render() -> None:
    """Перевіряє обчислення та форматування вкладених дерев виразів."""
    # ((x + 3) * (y + 2))
    ast: Expr = Mul(Add(Var("x"), Num(3)), Add(Var("y"), Num(2)))
    assert eval_expr(ast, {"x": 4, "y": 5}) == 49
    assert render(ast, "infix") == "((x + 3) * (y + 2))"
    assert render(ast, "prefix") == "(* (+ x 3) (+ y 2))"
    assert format_via_protocol(RenderableExpr(ast), "infix") == "((x + 3) * (y + 2))"
    assert collect_variables(ast) == frozenset({"x", "y"})


def test_substitute_preserves_original_ast() -> None:
    """Перевіряє чисту часткову та повну підстановку змінних без мутації."""
    ast: Expr = Add(Mul(Var("a"), Num(2)), Var("b"))

    partial_ast = substitute(ast, {"a": 10})
    assert render(partial_ast) == "((10 * 2) + b)"
    assert render(ast) == "((a * 2) + b)"

    full_ast = substitute(partial_ast, {"b": 5})
    assert render(full_ast) == "((10 * 2) + 5)"
    assert eval_expr(full_ast) == 25


def test_missing_variable_and_overflow_errors() -> None:
    """Перевіряє обробку відсутньої змінної та переповнення діапазону."""
    ast: Expr = Add(Var("x"), Var("missing_var"))
    with pytest.raises(UndefinedVariableError) as exc_info:
        eval_expr(ast, {"x": 1})
    assert exc_info.value.var_name == "missing_var"

    huge: Expr = Mul(Num(10_000), Num(1_000))
    with pytest.raises(EvalOverflowError):
        eval_expr(huge)
