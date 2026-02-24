from django.db.models import FilteredRelation, Q, F
from django.core.exceptions import FieldError
from django.db.utils import OperationalError
from app.models import Author
from app.models import Book

import traceback

def filteredrelation_alias(payload: str):
    """
    Fuzz the alias name of FilteredRelation. Past CVEs allowed SQL injection
    when alias names weren't sanitized.
    """
    # print("payload: "+str(payload))
    # qs = Book.objects.annotate(**{payload: FilteredRelation("author")}).values(payload)
    try:
        # Annotate using the fuzzed alias
        print("Payload string: "+str(payload))
        qs = Book.objects.annotate(**{
            payload: FilteredRelation("author")
        }).values(payload)
        return str(qs.query)
    except (FieldError, ValueError, TypeError) as e:
        print("exception:", e)
        print(traceback.format_exc())
        return
    return
