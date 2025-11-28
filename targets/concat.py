from django.db.models.functions import Concat
from django.db.models import Value, CharField
from app.models import Author

def concat_test(payload: str):
    try:
        qs = Author.objects.annotate(
            c=Concat(
                Value(payload),
                Value("test"),
                output_field=CharField()
            )
        )
        list(qs)
    except Exception:
        return

