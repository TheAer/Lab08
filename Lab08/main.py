"""Демонстраційний запуск лабораторної роботи №8 (Варіант 3: Калькулятор зі змінними)."""

from __future__ import annotations

from evaluator import (
    UndefinedVariableError,
    collect_variables,
    eval_expr,
    substitute,
)
from model import Add, Expr, Mul, Num, Var
from pretty import RenderableExpr, format_via_protocol, render


def main() -> None:
    """Демонструє побудову AST, підстановку змінних, обчислення та pretty-print."""
    # Вираз: ((x + 3) * (y + 2))
    expr: Expr = Mul(Add(Var("x"), Num(3)), Add(Var("y"), Num(2)))
    env: dict[str, int] = {"x": 4, "y": 5}

    print("1. Початковий вираз (infix): ", render(expr, "infix"))
    print(
        "2. Початковий вираз (prefix):",
        format_via_protocol(RenderableExpr(expr), "prefix"),
    )
    print("3. Змінні у виразі:          ", sorted(collect_variables(expr)))

    # Часткова підстановка лише змінної x=4 (y залишається символьною змінною)
    partially_substituted = substitute(expr, {"x": 4})
    print("4. Після підстановки x=4:    ", render(partially_substituted))

    # Повне обчислення у середовищі env
    result = eval_expr(expr, env)
    print(f"5. Значення при {env}: {result}")

    # Демонстрація обробки відсутньої змінної
    try:
        eval_expr(expr, {"x": 4})
    except UndefinedVariableError as exc:
        print(f"6. Очікувана помилка:        {exc}")


if __name__ == "__main__":
    main()
