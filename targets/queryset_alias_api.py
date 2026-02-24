# fuzzer/targets/queryset_alias_api.py
from django.db.models import F
from app.models import Company

def qs_alias_api(payload):
    qs = Company.objects.alias(**{payload: F("id")})
    list(qs)
    return str(qs.query)
