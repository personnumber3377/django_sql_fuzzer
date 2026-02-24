# fuzzer/targets/queryset_extra.py
from app.models import Author

def qs_extra(payload):
    qs = Author.objects.extra(
        select={payload: f"id || '{payload}'"},
        where=[f"name LIKE '%{payload}%'"],
        tables=[payload],
    )
    list(qs)
    return str(qs.query)
    