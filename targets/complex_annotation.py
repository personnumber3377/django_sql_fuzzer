# targets/complex_annotation.py

from django.db.models import (
    F,
    Value,
    Case,
    When,
    Subquery,
    Exists,
    OuterRef,
)
from django.core.exceptions import FieldError
from django.db.utils import OperationalError

from app.models import Book


def complex_annotation(payload: str):
    """
    Fuzz complex annotation expressions that SHOULD require an alias.

    Django requires:
        Book.objects.annotate(alias=EXPR)
    NOT:
        Book.objects.annotate(EXPR)

    Past/future bugs in this area can cause compiler crashes or SQL errors.
    """

    # Pretend the payload is a field name or literal injected into expressions.
    try:
        # Construct fuzzed components using attacker-controlled payload
        exprs = [
            F(payload) * F(payload),
            Value(payload),
            Case(
                When(**{f"{payload}__gte": 400}, then=Value(payload)),
                default=Value(payload),
            ),
            Subquery(
                Book.objects.filter(**{f"{payload}__id": OuterRef("pk")})
                .order_by(payload)
                .values(payload)[:1]
            ),
            Exists(Book.objects.filter(**{f"{payload}__id": OuterRef("pk")})),
        ]

        for expr in exprs:
            # This is the vulnerable pattern: complex annotation w/out alias
            qs = Book.objects.annotate(expr)

            # Force evaluation
            list(qs)

    except (FieldError, ValueError, TypeError, OperationalError):
        # Safe compiler/ORM errors → acceptable
        return
