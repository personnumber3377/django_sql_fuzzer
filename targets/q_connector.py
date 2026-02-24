from django.db.models import Q
from django.core.exceptions import FieldError
from app.models import Author

def q_connector(payload: str):
    """
    Past vulnerability: custom Q._connector strings could break SQL generation.
    """
    q = Q(name="test")
    q._connector = payload  # dangerous
    qs = Author.objects.filter(q)
    list(qs) # Actually execute the query
    return str(qs.query)
