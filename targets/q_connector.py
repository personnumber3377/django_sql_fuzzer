from django.db.models import Q
from django.core.exceptions import FieldError
from app.models import Author

def q_connector(payload: str):
    """
    Past vulnerability: custom Q._connector strings could break SQL generation.
    """
    try:
        q = Q(name="test")
        q._connector = payload  # dangerous
        Author.objects.filter(q).exists()
    except Exception:
        return