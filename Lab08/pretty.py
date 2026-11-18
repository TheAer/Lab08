"""Текстове представлення виразів (pretty-print) із використанням Literal та Protocol."""

from __future__ import annotations

from dataclasses import dataclass

from model import Add, Expr, Mul, Num, RenderStyle, SupportsRender, Var


def render(expr: Expr, style: RenderStyle = "infix") -> str:
    """Перетворює дерево виразу Expr у рядок у форматі 'infix' або 'prefix'."""
    match expr:
        case Num(value=v):
            return str(v)
        case Var(name=name):
            return name
        case Add(left=left, right=right):
            left_s = render(left, style)
            right_s = render(right, style)
            return (
                f"(+ {left_s} {right_s})"
                if style == "prefix"
                else f"({left_s} + {right_s})"
            )
        case Mul(left=left, right=right):
            left_s = render(left, style)
            right_s = render(right, style)
            return (
                f"(* {left_s} {right_s})"
                if style == "prefix"
                else f"({left_s} * {right_s})"
            )


@dataclass(frozen=True)
class RenderableExpr:
    """Незмінна обгортка над Expr, що структурно задовольняє протокол SupportsRender."""

    expr: Expr

    def render(self, style: RenderStyle = "infix") -> str:
        return render(self.expr, style)


def format_via_protocol(item: SupportsRender, style: RenderStyle = "infix") -> str:
    """Демонструє структурну типізацію (Protocol) без успадкування."""
    return item.render(style)
