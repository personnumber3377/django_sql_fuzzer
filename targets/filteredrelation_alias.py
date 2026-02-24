from django.db.models import FilteredRelation, Q, F
from django.core.exceptions import FieldError
from django.db.utils import OperationalError
from app.models import Author
from app.models import Book

def filteredrelation_alias(payload: str):
    """
    Fuzz the alias name of FilteredRelation. Past CVEs allowed SQL injection
    when alias names weren't sanitized.
    """
    # print("payload: "+str(payload))

    try:
        # Annotate using the fuzzed alias
        qs = Book.objects.annotate(**{
            payload: FilteredRelation("author")
        }).values(payload)

        # Force SQL generation containing the annotation alias
        # print(qs.explain())         # <--- absolutely required

        # Force Django to SELECT the annotation column
        # print("payload: "+str(payload))
        # print("HERE IS THE EXECUTED SQL STUFF: "+str(qs.query))

        # list(qs)    # <--- also required
        return str(qs.query)
    except (FieldError, ValueError, TypeError) as e:
        # print("exception:", e)
        return
    return