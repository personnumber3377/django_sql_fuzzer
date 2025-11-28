# fuzzer/targets/q_connector.py
from django.db.models import Q
from app.models import Author

def q_connector(payload):
    q = Q(name=payload, _connector=payload)
    qs = Author.objects.filter(q)
    list(qs)
