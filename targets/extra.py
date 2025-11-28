from django.db import connection
from django.db.utils import OperationalError, ProgrammingError
from app.models import Book

def extra(payload: str):
    """
    Fuzz the dangerous extra(where/select/tables) API.
    This API directly inserts payloads into SQL fragments.
    """
    try:
        qs = Book.objects.extra(
            where=[payload],
            select={"p": payload},
            tables=[payload],
        )
        list(qs)
    except (OperationalError, ValueError, TypeError):
        return
