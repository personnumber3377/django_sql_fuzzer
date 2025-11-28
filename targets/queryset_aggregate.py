from django.db.models import Avg
from app.models import Company

def qs_agg(payload: str):
    try:
        Company.objects.aggregate(**{payload: Avg("num_employees")})
    except Exception:
        return
