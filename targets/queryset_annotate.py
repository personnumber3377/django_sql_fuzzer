from django.db.models import F, Value, CharField
from django_sql_fuzzer.app.models import Author

def qs_annotate(payload: str):
    try:
        qs = Author.objects.annotate(**{
            payload: F("age") + Value(1)
        })
        list(qs)
    except Exception:
        return
