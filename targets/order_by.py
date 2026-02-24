from django.core.exceptions import FieldError
from django.db.utils import OperationalError, ProgrammingError
from app.models import Book

def order_by(payload: str):
    """
    Fuzz identifier injection through order_by(), which is not fully quoted
    because Django treats them as field references.
    """
    try:
        qs = Book.objects.order_by(payload)
        list(qs)
        return str(qs.query)
    except (FieldError, ValueError, TypeError):
        return str(qs.query)
