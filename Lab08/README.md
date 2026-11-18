# Лабораторна робота №8. Алгебраїчні типи даних “по-Python’івськи”

**Варіант 3:** Калькулятор зі змінними (`Num`, `Var`, `Add`, `Mul`).

## Опис моделі та модулів
- `model.py` — незмінні dataclass-вузли (`@dataclass(frozen=True)`), рекурсивне об'єднання `Expr: TypeAlias = Union[Num, Var, Add, Mul]`, обмеження `RenderStyle = Literal["infix", "prefix"]` та структурний протокол `SupportsRender(Protocol)`.
- `evaluator.py` — чисті функції `eval_expr(expr, env)`, `substitute(expr, env)` і `collect_variables(expr)` на основі `match/case`, з обробкою відсутніх змінних (`UndefinedVariableError`).
- `pretty.py` — текстовий рендер `render(expr, style)` та адаптер `RenderableExpr`.
- `main.py` — демонстраційний запуск.
- `tests/test_expr.py` — модульні тести `pytest`.

## Запуск та перевірка

```bash
python main.py
python -m pytest -v
mypy --strict model.py evaluator.py pretty.py main.py tests
