from django.db.models import Avg
from app.models import Company

def qs_agg(payload: str):
    qs = Company.objects.aggregate(**{payload: Avg("num_employees")})
    return str(qs.query)
