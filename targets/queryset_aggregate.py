from django.db.models import Avg
from app.models import Company
from django.db.utils import OperationalError, ProgrammingError

def qs_agg(payload: str):
    try:
        qs = Company.objects.aggregate(**{payload: Avg("num_employees")})
        list(qs)
    except ProgrammingError:
        return None
    return None # 'dict' object has no attribute 'query' has no attribute dict # qs.query
