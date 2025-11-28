from django.db.models import Window, F
from django.db.models.functions import RowNumber
from django.db.utils import OperationalError, ProgrammingError
from app.models import Book

def window(payload: str):
    """
    Fuzz identifier-like uses in Window() OVER clauses.
    """
    try:
        qs = Book.objects.annotate(
            rn=Window(
                expression=RowNumber(),
                partition_by=[F(payload)],
                order_by=[payload],
            )
        )
        list(qs)
    except (OperationalError, ProgrammingError, ValueError, TypeError):
        return

