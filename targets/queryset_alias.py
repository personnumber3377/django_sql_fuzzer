from django.db.models import F
from app.models import Company
from django.core.exceptions import FieldError

def qs_alias_api(payload: str):
    qs = Company.objects.alias(**{payload: F("id")})
    list(qs)
    return str(qs.query)