# fuzzer/targets/queryset_alias.py
from django.db.models import F
from app.models import Company

def qs_alias(payload: str):
    qs = Company.objects.values(**{payload: F("ceo__salary")})
    list(qs)
