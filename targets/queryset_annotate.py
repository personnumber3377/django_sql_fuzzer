from django.db.models import F, Value, CharField
from app.models import Author

def qs_annotate(payload: str):
    qs = Author.objects.annotate(**{
        payload: F("age") + Value(1)
    })
    list(qs)
    return str(qs.query)
